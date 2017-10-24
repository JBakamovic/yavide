import logging
import multiprocessing
import os
import shlex
import subprocess
import sqlite3
import time
import tempfile
from services.parser.ast_node_identifier import ASTNodeId
from services.parser.clang_parser import ChildVisitResult
from services.parser.clang_parser import ClangParser

# TODO move this to utils
import itertools
def slice_it(iterable, n, padvalue=None):
    return itertools.izip_longest(*[iter(iterable)]*n, fillvalue=padvalue)

class SymbolDatabase(object):
    def __init__(self, db_filename = None):
        self.filename = db_filename
        if db_filename:
            self.db_connection = sqlite3.connect(db_filename)
        else:
            self.db_connection = None

    def __del__(self):
        if self.db_connection:
            self.db_connection.close()

    def open(self, db_filename):
        if not self.db_connection:
            self.db_connection = sqlite3.connect(db_filename)
            self.filename = db_filename

    def close(self):
        if self.db_connection:
            self.db_connection.close()
            self.db_connection = None

    def get_all(self):
        # TODO Use generators
        return self.db_connection.cursor().execute('SELECT * FROM symbol')

    def get_by_id(self, id):
        return self.db_connection.cursor().execute('SELECT * FROM symbol WHERE usr=?', (id,))

    def insert_single(self, filename, unique_id, line, column, symbol_type):
        self.db_connection.cursor().execute('INSERT INTO symbol VALUES (?, ?, ?, ?, ?)', (filename, unique_id, line, column, symbol_type,))

    def flush(self):
        self.db_connection.commit()

    def delete(self, filename):
        self.db_connection.cursor().execute('DELETE FROM symbol WHERE filename=?', (filename,))

    def delete_all(self):
        self.db_connection.cursor().execute('DELETE FROM symbol')

    def create_data_model(self):
        self.db_connection.cursor().execute('CREATE TABLE IF NOT EXISTS symbol_type (id integer, name text, PRIMARY KEY(id))')
        self.db_connection.cursor().execute('CREATE TABLE IF NOT EXISTS symbol (filename text, usr text, line integer, column integer, type integer, PRIMARY KEY(filename, usr, line, column), FOREIGN KEY (type) REFERENCES symbol_type(id))')
        symbol_types = [(1, 'function'), (2, 'variable'), (3, 'user_defined_type'), (4, 'macro'),]
        self.db_connection.cursor().executemany('INSERT INTO symbol_type VALUES (?, ?)', symbol_types)


class ClangIndexer(object):
    def __init__(self, parser, callback = None):
        self.callback = callback
        self.symbol_db_name = '.yavide_index.db'
        self.symbol_db = SymbolDatabase()
        self.proj_root_directory = None
        self.compiler_args = None
        self.parser = parser
        self.op = {
            0x0 : self.__run_on_single_file,
            0x1 : self.__run_on_directory,
            0x2 : self.__drop_single_file,
            0x3 : self.__drop_all,
            0x10 : self.__go_to_definition,
            0x11 : self.__find_all_references
        }

    def __call__(self, args):
        self.op.get(int(args[0]), self.__unknown_op)(int(args[0]), args[1:len(args)])

    def __unknown_op(self, id, args):
        logging.error("Unknown operation with ID={0} triggered! Valid operations are: {1}".format(id, self.op))

    def __run_on_single_file(self, id, args):
        self.proj_root_directory = str(args[0])
        contents_filename        = str(args[1])
        original_filename        = str(args[2])
        self.compiler_args       = str(args[3])

        # We don't run indexer on files modified but not saved
        if contents_filename == original_filename:
            self.symbol_db.open(os.path.join(self.proj_root_directory, self.symbol_db_name))
            self.symbol_db.delete(original_filename)
            index_single_file(self.parser, self.proj_root_directory, contents_filename, original_filename, compiler_args, self.symbol_db)

        if self.callback:
            self.callback(id, args)

    def __run_on_directory(self, id, args):
        self.proj_root_directory = str(args[0])
        self.compiler_args       = str(args[1])

        # Do not run indexer on whole directory if we already did it
        directory_already_indexed = True
        indexer_db = os.path.join(self.proj_root_directory, self.symbol_db_name)
        if not os.path.exists(indexer_db):
            directory_already_indexed = False

        # Otherwise, index the whole directory
        if not directory_already_indexed:
            logging.info("Starting to index whole directory '{0}' ... ".format(self.proj_root_directory))

            # Open and initialize the symbol database
            self.symbol_db.open(indexer_db)
            self.symbol_db.create_data_model()

            # Build-up a list of source code files from given project directory
            cpp_file_list = []
            for dirpath, dirs, files in os.walk(self.proj_root_directory):
                for file in files:
                    name, extension = os.path.splitext(file)
                    if extension in ['.cpp', '.cc', '.cxx', '.c', '.h', '.hh', '.hpp']:
                        cpp_file_list.append(os.path.join(dirpath, file))

            # We will need a full path to 'clang_index.py' script
            this_script_directory = os.path.dirname(os.path.realpath(__file__))
            clang_index_script = os.path.join(this_script_directory, 'clang_index.py')

            # We will also need to setup a correct PYTHONPATH in order to run 'clang_index.py' script from another process(es)
            my_env = os.environ.copy()
            my_env["PYTHONPATH"] = os.path.dirname(os.path.dirname(this_script_directory))

            process_list = []
            tmp_db_list = []

            # We will slice the input file list into a number of chunks which corresponds to the amount of available CPU cores
            how_many_chunks = len(cpp_file_list) / multiprocessing.cpu_count()

            # Now we are able to parallelize the indexing operation across different CPU cores
            for cpp_file_list_chunk in slice_it(cpp_file_list, how_many_chunks):
                # 'slice_it()' utility function may return None's as part of the slice (to fill up the slice up to the given length)
                chunk_with_no_none_items = ', '.join(item for item in cpp_file_list_chunk if item)

                # Each subprocess will get an empty DB file to record indexing results into it
                handle, tmp_db = tempfile.mkstemp(suffix='.indexer.db', dir=self.proj_root_directory)

                # Start indexing a given chunk in a new subprocess
                #   Note: Running and handling subprocesses as following, and not via multiprocessing.Process module,
                #         is done intentionally and more or less it served as a (very ugly) workaround because of several reasons:
                #           (1) 'libclang' is not made thread safe which is why we want to utilize it from different
                #               processes (e.g. each process will get its own instance of 'libclang')
                #           (2) Python bindings for 'libclang' implement some sort of module caching mechanism which basically
                #               contradicts with the intent from (1)
                #           (3) Point (2) seems to be a Pythonic way of implementing modules which basically obscures
                #               the way how different instances of libraries (modules?) across different processes
                #               should behave
                #           (4) Python does have a way to handle such situations (module reloading) but seems that it
                #               works only for the simplest cases which is unfortunally not the case here
                #           (5) Creating a new process via subprocess.Popen interface and running the indexing operation
                #               from another Python script ('clang_index.py') is the only way how I managed to get it
                #               working correctly (each process will get their own instance of library)
                cmd = "python2 " + clang_index_script + " --project_root_directory='" \
                    + self.proj_root_directory + "' --compiler_args='" + self.compiler_args + "' --filename_list='" \
                    + chunk_with_no_none_items + "' --output_db_filename='" + tmp_db + "' " + "--log_file='" + \
                    logging.getLoggerClass().root.handlers[0].baseFilename + "'"
                p = subprocess.Popen(shlex.split(cmd), env=my_env)

                # Store handles to subprocesses and corresponding DB files so we can handle them later on
                process_list.append(p)
                tmp_db_list.append((handle, tmp_db))

            # Wait subprocesses to finish with their work
            for p in process_list:
                p.wait()

            # Merge the results of indexing operations (each process created a single indexing DB)
            logging.info('about to start merging the databases ... ' + str(tmp_db_list))
            for handle, db in tmp_db_list:
                tmp_symbol_db = SymbolDatabase(db)
                symbols = tmp_symbol_db.get_all()
                if symbols:
                    for s in symbols:
                        self.symbol_db.insert_single(s[0], s[1], s[2], s[3], s[4])
                self.symbol_db.flush()
                tmp_symbol_db.close()
                os.close(handle)
                os.remove(db)

            # TODO how to count total CPU time, for all sub-processes?
            logging.info("Indexing {0} is completed.".format(self.proj_root_directory))
        else:
            logging.info("Directory '{0}' already indexed ... ".format(self.proj_root_directory))

        if self.callback:
            self.callback(id, args)

    def __drop_single_file(self, id, args):
        self.symbol_db.delete(filename)
        if self.callback:
            self.callback(id, args)

    def __drop_all(self, id, args):
        delete_file = bool(args[0])
        self.symbol_db.delete_all()
        if delete_file:
            self.symbol_db.close()
            os.remove(self.symbol_db.filename)
            logging.info('DB file removed ...')

        if self.callback:
            self.callback(id, args)

    def __go_to_definition(self, id, args):
        cursor = self.parser.get_definition(
            self.parser.parse(
                str(args[0]),
                str(args[0]), # TODO make it work on edited files (we need modified here)
                self.compiler_args,
                self.proj_root_directory
            ),
            int(args[1]), int(args[2])
        )
        if cursor:
            logging.info('Definition location {0}'.format(str(cursor.location)))
        else:
            logging.info('No definition found.')

        if self.callback:
            self.callback(id, cursor.location if cursor else None)

    def __find_all_references(self, id, args):
        start = time.clock()
        references = []
        tunit = self.parser.parse(str(args[0]), str(args[0]), self.compiler_args, self.proj_root_directory)
        if tunit:
            cursor = self.parser.get_cursor(tunit, int(args[1]), int(args[2]))
            if cursor:
                logging.info("Finding all references of cursor [{0}, {1}]: {2}. name = {3}".format(cursor.location.line, cursor.location.column, tunit.spelling, cursor.displayname))
                usr = cursor.referenced.get_usr() if cursor.referenced else cursor.get_usr()
                ast_node_id = self.parser.get_ast_node_id(cursor)
                if ast_node_id in [ASTNodeId.getFunctionId(), ASTNodeId.getMethodId()]:
                    symbols = self.symbol_db.get_by_id(usr)
                elif ast_node_id in [ASTNodeId.getClassId(), ASTNodeId.getStructId(), ASTNodeId.getEnumId(), ASTNodeId.getEnumValueId(), ASTNodeId.getUnionId(), ASTNodeId.getTypedefId()]:
                    symbols = self.symbol_db.get_by_id(usr)
                elif ast_node_id in [ASTNodeId.getLocalVariableId(), ASTNodeId.getFunctionParameterId(), ASTNodeId.getFieldId()]:
                    symbols = self.symbol_db.get_by_id(usr)
                elif ast_node_id in [ASTNodeId.getMacroDefinitionId(), ASTNodeId.getMacroInstantiationId()]:
                    symbols = self.symbol_db.get_by_id(usr)
                else:
                    symbols = None

                if symbols:
                    for symbol in symbols:
                        references.append((symbol[0], symbol[1], symbol[2], symbol[3]))
                        logging.debug('symbol: ' + str(symbol))

                time_elapsed = time.clock() - start
                logging.info('Find-all-references operation of {0} took {1}: {2}'.format(cursor.displayname, time_elapsed, str(references)))

        if self.callback:
            self.callback(id, references)


def index_file_list(proj_root_directory, compiler_args, filename_list, output_db_filename):
    symbol_db = SymbolDatabase(output_db_filename)
    symbol_db.create_data_model()
    parser = ClangParser()
    for filename in filename_list:
        index_single_file(parser, proj_root_directory, filename, filename, compiler_args, symbol_db)
    symbol_db.close()


def index_single_file(parser, proj_root_directory, contents_filename, original_filename, compiler_args, symbol_db):
    def visitor(ast_node, ast_parent_node, parser):
        if (ast_node.location.file and ast_node.location.file.name == tunit.spelling):  # we are not interested in symbols which got into this TU via includes
            id = parser.get_ast_node_id(ast_node)
            usr = ast_node.referenced.get_usr() if ast_node.referenced else ast_node.get_usr()
            line = int(parser.get_ast_node_line(ast_node))
            column = int(parser.get_ast_node_column(ast_node))
            try:
                if id in [ASTNodeId.getFunctionId(), ASTNodeId.getMethodId()]:
                    symbol_db.insert_single(tunit.spelling, usr, line, column, 1,)
                elif id in [ASTNodeId.getClassId(), ASTNodeId.getStructId(), ASTNodeId.getEnumId(), ASTNodeId.getEnumValueId(), ASTNodeId.getUnionId(), ASTNodeId.getTypedefId()]:
                    symbol_db.insert_single(tunit.spelling, usr, line, column, 3,)
                elif id in [ASTNodeId.getLocalVariableId(), ASTNodeId.getFunctionParameterId(), ASTNodeId.getFieldId()]:
                    symbol_db.insert_single(tunit.spelling, usr, line, column, 2,)
                elif id in [ASTNodeId.getMacroDefinitionId(), ASTNodeId.getMacroInstantiationId()]:
                    symbol_db.insert_single(tunit.spelling, usr, line, column, 4,)
                else:
                    pass
            except sqlite3.IntegrityError:
                pass
            return ChildVisitResult.RECURSE.value  # If we are positioned in TU of interest, then we'll traverse through all descendants
        return ChildVisitResult.CONTINUE.value  # Otherwise, we'll skip to the next sibling

    logging.info("Indexing a file '{0}' ... ".format(original_filename))

    # Index a single file
    start = time.clock()
    tunit = parser.parse(contents_filename, original_filename, str(compiler_args), proj_root_directory)
    if tunit:
        parser.traverse(tunit.cursor, parser, visitor)
        symbol_db.flush()
    time_elapsed = time.clock() - start
    logging.info("Indexing {0} took {1}.".format(original_filename, time_elapsed))

