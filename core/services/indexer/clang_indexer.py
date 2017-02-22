import logging
import time
import os


class ClangIndexer():
    def __init__(self, parser, callback = None):
        self.parser = parser
        self.callback = callback
        self.op = {
            0x0 : self.__load_from_disk,
            0x1 : self.__save_to_disk,
            0x2 : self.__run_on_single_file,
            0x3 : self.__run_on_directory,
            0x4 : self.__drop_single_file,
            0x5 : self.__drop_all,
            0x10 : self.__go_to_definition,
            0x11 : self.__find_all_references
        }

    def __call__(self, args):
        self.op.get(int(args[0]), self.__unknown_op)(args[1:len(args)])

    def __unknown_op(self):
        pass

    def __load_from_disk(self, args):
        start = time.clock()
        self.parser.load_from_disk(str(args[0]))
        time_elapsed = time.clock() - start
        logging.info("Loading from {0} took {1}.".format(str(args[0]), time_elapsed))

    def __save_to_disk(self, args):
        start = time.clock()
        self.parser.save_to_disk(str(args[0]))
        time_elapsed = time.clock() - start
        logging.info("Saving to {0} took {1}.".format(str(args[0]), time_elapsed))

    def __run_on_single_file(self, args):
        proj_root_directory = str(args[0])
        filename = str(args[1])
        compiler_args = list(str(args[2]).split())
        logging.info("Indexing a single file '{0}' ... ".format(filename))

        # TODO Run this in a separate non-blocking process
        # Index a single file
        start = time.clock()
        self.parser.run(filename, filename, compiler_args, proj_root_directory)
        time_elapsed = time.clock() - start
        logging.info("Indexing {0} took {1}.".format(filename, time_elapsed))

    def __run_on_directory(self, args):
        proj_root_directory = str(args[0])
        compiler_args = list(str(args[1]).split())
        logging.info("Indexing a whole project '{0}' ... ".format(proj_root_directory))

        # TODO Run this in a separate non-blocking process
        # Index each file in project root directory
        start = time.clock()
        self.parser.drop_ast_node_list()
        for dirpath, dirs, files in os.walk(proj_root_directory):
            for file in files:
                name, extension = os.path.splitext(file)
                if extension in ['.cpp', '.cc', '.cxx', '.c', '.h', '.hh', '.hpp']:
                    full_path = os.path.join(dirpath, file)
                    logging.info("Indexing ... {0}".format(full_path))
                    self.parser.run(full_path, full_path, compiler_args, proj_root_directory)
        time_elapsed = time.clock() - start
        logging.info("Indexing {0} took {1}.".format(proj_root_directory, time_elapsed))

    def __drop_single_file(self, args):
        self.parser.drop_ast_node(str(args[0]))

    def __drop_all(self, dummy = 0):
        self.parser.drop_ast_node_list()

    def __go_to_definition(self, args):
        cursor = self.parser.get_definition(str(args[0]), str(args[1]), int(args[2]), int(args[3]))
        if cursor:
            logging.info("go_to_definition() location %s" % str(cursor.location))

        if self.callback:
            self.callback.go_to_definition(cursor, args)

    def __find_all_references(self, args):
        references = self.parser.find_all_references(str(args[0]), str(args[1]), int(args[2]), int(args[3]))
        logging.info("find_all_references():")
        for r in references:
            logging.info("Ref location %s" % str(r))
