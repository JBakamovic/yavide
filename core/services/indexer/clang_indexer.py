import logging
import multiprocessing
import os
import shlex
import subprocess
import time
import tempfile
from services.parser.ast_node_identifier import ASTNodeId
from services.parser.clang_parser import ChildVisitResult
from services.parser.clang_parser import ClangParser
from services.parser.tunit_cache import NoCache
from services.indexer.symbol_database import SymbolDatabase

# TODO move this to utils
import itertools
def slice_it(iterable, n, padvalue=None):
    return itertools.izip_longest(*[iter(iterable)]*n, fillvalue=padvalue)

class ClangIndexer(object):
    def __init__(self, parser, root_directory, callback = None):
        self.callback = callback
        self.symbol_db_name = '.yavide_index.db'
        self.symbol_db = SymbolDatabase()
        self.parser = parser
        self.root_directory = root_directory
        self.op = {
            0x0 : self.__run_on_single_file,
            0x1 : self.__run_on_directory,
            0x2 : self.__drop_single_file,
            0x3 : self.__drop_all,
            0x10 : self.__find_all_references
        }

    def get_symbol_db(self):
        return self.symbol_db

    def __call__(self, args):
        self.op.get(int(args[0]), self.__unknown_op)(int(args[0]), args[1:len(args)])

    def __unknown_op(self, id, args):
        logging.error("Unknown operation with ID={0} triggered! Valid operations are: {1}".format(id, self.op))

    def __run_on_single_file(self, id, args):
        contents_filename = str(args[0])
        original_filename = str(args[1])

        # We don't run indexer on files modified but not saved
        if contents_filename == original_filename:
            self.symbol_db.open(os.path.join(self.root_directory, self.symbol_db_name))
            self.symbol_db.delete(get_basename(self.root_directory, original_filename))
            index_single_file(
                self.parser,
                self.root_directory,
                contents_filename,
                original_filename,
                self.symbol_db
            )

        if self.callback:
            self.callback(id, args)

    def __run_on_directory(self, id, args):
        # Do not run indexer on whole directory if we already did it
        directory_already_indexed = True
        indexer_db = os.path.join(self.root_directory, self.symbol_db_name)
        if not os.path.exists(indexer_db):
            directory_already_indexed = False

        # We still need to establish the database connection even if we don't go into indexing
        self.symbol_db.open(indexer_db)

        # Otherwise, index the whole directory
        if not directory_already_indexed:
            logging.info("Starting to index whole directory '{0}' ... ".format(self.root_directory))

            # When creating the symbol db for the first time we need to create a data model for it
            self.symbol_db.create_data_model()

            # Build-up a list of source code files from given project directory
            cpp_file_list = []
            for dirpath, dirs, files in os.walk(self.root_directory):
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
            tmp_filename_list = []

            # We will slice the input file list into a number of chunks which corresponds to the amount of available CPU cores
            how_many_chunks = len(cpp_file_list) / multiprocessing.cpu_count()

            # Now we are able to parallelize the indexing operation across different CPU cores
            for cpp_file_list_chunk in slice_it(cpp_file_list, how_many_chunks):
                # 'slice_it()' utility function may return None's as part of the slice (to fill up the slice up to the given length)
                chunk_with_no_none_items = '\n'.join(item for item in cpp_file_list_chunk if item)

                # Each subprocess will get a file containing source files to be indexed
                cpp_file_list_handle, cpp_file_list = tempfile.mkstemp(prefix='.yavide_idx_input', dir=self.root_directory)
                os.write(cpp_file_list_handle, chunk_with_no_none_items)
                os.close(cpp_file_list_handle)

                # Each subprocess will get an empty DB file to record indexing results into it
                tmp_db_handle, tmp_db = tempfile.mkstemp(prefix=self.symbol_db_name, dir=self.root_directory)
                os.close(tmp_db_handle)

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
                cmd = "python2 " + clang_index_script + \
                        "  --project_root_directory='" + self.root_directory + \
                        "' --compiler_args_filename='" + self.parser.get_compiler_args_db().filename() + \
                        "' --input_list='" + cpp_file_list + \
                        "' --output_db_filename='" + tmp_db + \
                        "' " + "--log_file='" + logging.getLoggerClass().root.handlers[0].baseFilename + '_' + str(len(process_list)+1) + "'"
                p = subprocess.Popen(shlex.split(cmd), env=my_env)

                # Store handles to subprocesses and corresponding tmp files so we can handle them later on
                process_list.append(p)
                tmp_db_list.append(tmp_db)
                tmp_filename_list.append(cpp_file_list)

            # Wait subprocesses to finish with their work
            for p in process_list:
                p.wait()

            # Merge the results of indexing operations
            for db in tmp_db_list:
                tmp_symbol_db = SymbolDatabase(db)
                symbols = tmp_symbol_db.get_all()
                if symbols:
                    for sym in symbols:
                        self.symbol_db.insert_single(sym[0], sym[1], sym[2], sym[3], sym[4], sym[5], sym[6])
                self.symbol_db.flush()
                tmp_symbol_db.close()
                os.remove(db)

            # Get rid of temporary files containing source filenames
            for f in tmp_filename_list:
                os.remove(f)

            # TODO how to count total CPU time, for all sub-processes?
            logging.info("Indexing {0} is completed.".format(self.root_directory))
        else:
            logging.info("Directory '{0}' already indexed ... ".format(self.root_directory))

        if self.callback:
            self.callback(id, args)

    def __drop_single_file(self, id, args):
        filename = str(args[0])
        self.symbol_db.delete(get_basename(self.root_directory, filename))
        if self.callback:
            self.callback(id, args)

    def __drop_all(self, id, args):
        delete_file_from_disk = bool(args[0])
        if delete_file_from_disk:
            self.symbol_db.close()
            os.remove(self.symbol_db.filename)
            logging.info('Indexer DB dropped.')

        if self.callback:
            self.callback(id, args)

    def __find_all_references(self, id, args):
        start = time.clock()
        references = ()
        tunit = self.parser.parse(str(args[0]), str(args[0]))
        if tunit:
            cursor = self.parser.get_cursor(tunit, int(args[1]), int(args[2]))
            if cursor:
                # TODO In order to make find-all-references work on edited (and not yet saved) files,
                #      we would need to manipulate directly with USR.
                #      In case of edited files, USR contains a name of a temporary file we serialized
                #      the contents in and therefore will not match the USR in the database (which in
                #      contrast contains an original filename).
                usr = cursor.referenced.get_usr() if cursor.referenced else cursor.get_usr()
                ast_node_id = self.parser.get_ast_node_id(cursor)
                if ast_node_id in [ASTNodeId.getFunctionId(), ASTNodeId.getMethodId()]:
                    references = self.symbol_db.get_by_id(usr).fetchall()
                elif ast_node_id in [ASTNodeId.getClassId(), ASTNodeId.getStructId(), ASTNodeId.getEnumId(), ASTNodeId.getEnumValueId(), ASTNodeId.getUnionId(), ASTNodeId.getTypedefId()]:
                    references = self.symbol_db.get_by_id(usr).fetchall()
                elif ast_node_id in [ASTNodeId.getLocalVariableId(), ASTNodeId.getFunctionParameterId(), ASTNodeId.getFieldId()]:
                    references = self.symbol_db.get_by_id(usr).fetchall()
                elif ast_node_id in [ASTNodeId.getMacroDefinitionId(), ASTNodeId.getMacroInstantiationId()]:
                    references = self.symbol_db.get_by_id(usr).fetchall()
                else:
                    pass
            logging.info("Find-all-references operation of '{0}', [{1}, {2}], '{3}' took {4}".format(cursor.displayname, cursor.location.line, cursor.location.column, tunit.spelling, time.clock() - start))

        if self.callback:
            self.callback(id, [args, references])

        logging.info("\n{0}".format('\n'.join(str(ref) for ref in references)))

def index_file_list(root_directory, input_filename_list, compiler_args_filename, output_db_filename):
    symbol_db = SymbolDatabase(output_db_filename)
    symbol_db.create_data_model()
    parser = ClangParser(compiler_args_filename, NoCache())
    with open(input_filename_list, 'r') as input_list:
        for filename in input_list:
            index_single_file(parser, root_directory, filename.strip(), filename.strip(), symbol_db)
    symbol_db.close()


def index_single_file(parser, root_directory, contents_filename, original_filename, symbol_db):
    def extract_cursor_context(filename, line):
        import linecache
        return linecache.getline(filename, line)

    def visitor(ast_node, ast_parent_node, parser):
        ast_node_location = ast_node.location
        ast_node_tunit_spelling = ast_node.translation_unit.spelling
        if (ast_node_location.file and ast_node_location.file.name == ast_node_tunit_spelling):  # we are not interested in symbols which got into this TU via includes
            id = parser.get_ast_node_id(ast_node)
            usr = ast_node.referenced.get_usr() if ast_node.referenced else ast_node.get_usr()
            line = int(parser.get_ast_node_line(ast_node))
            column = int(parser.get_ast_node_column(ast_node))
            if id in [
                ASTNodeId.getClassId(), ASTNodeId.getStructId(), ASTNodeId.getEnumId(), ASTNodeId.getEnumValueId(), # handle user-defined types
                ASTNodeId.getUnionId(), ASTNodeId.getTypedefId(), ASTNodeId.getUsingDeclarationId(),
                ASTNodeId.getFunctionId(), ASTNodeId.getMethodId(),                                                 # handle functions and methods
                ASTNodeId.getLocalVariableId(), ASTNodeId.getFunctionParameterId(), ASTNodeId.getFieldId(),         # handle local/function variables and member variables
                ASTNodeId.getMacroDefinitionId(), ASTNodeId.getMacroInstantiationId()                               # handle macros
            ]:
                symbol_db.insert_single(
                    get_basename(root_directory, ast_node_tunit_spelling),
                    line,
                    column,
                    usr,
                    extract_cursor_context(ast_node_tunit_spelling, line),
                    ast_node.referenced._kind_id if ast_node.referenced else ast_node._kind_id,
                    ast_node.is_definition()
                )
            else:
                pass
            return ChildVisitResult.RECURSE.value  # If we are positioned in TU of interest, then we'll traverse through all descendants
        return ChildVisitResult.CONTINUE.value  # Otherwise, we'll skip to the next sibling

    logging.info("Indexing a file '{0}' ... ".format(original_filename))

    # Index a single file
    start = time.clock()
    tunit = parser.parse(contents_filename, original_filename)
    if tunit:
        parser.traverse(tunit.cursor, parser, visitor)
        symbol_db.flush()
    time_elapsed = time.clock() - start
    logging.info("Indexing {0} took {1}.".format(original_filename, time_elapsed))

def get_basename(root_dir, full_path):
    return full_path[len(root_dir):].lstrip(os.sep)
