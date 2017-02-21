import logging
import time
import os
from services.parser.clang_parser import ClangParser


class ClangIndexer():
    def __init__(self, parser, callback = None):
        self.parser = parser
        self.callback = callback
        self.op = {
            0x0 : self.__load_from_disk,
            0x1 : self.__save_to_disk,
            0x2 : self.__start_indexer,
            0x3 : self.__go_to_definition,
            0x4 : self.__find_all_references
        }

    def __call__(self, args):
        self.op.get(int(args[0]), self.__unknown_op)(args[1:len(args)])

    def __unknown_op(self):
        pass

    def __start_indexer(self, args):
        # TODO Project has been already indexed?
        #       1. If yes, then reload the serialized AST's
        #           * It might be that source code has been modified outside the IDE,
        #             in which case we will want to rerun indexer on those files
        #       2. Otherwise, start indexing the whole project (might take a while)

        proj_root_directory = str(args[0])
        compiler_args = list(str(args[1]).split())
        logging.info("Starting indexing {0} ... ".format(proj_root_directory))

        # Index each file in project root directory
        for dirpath, dirs, files in os.walk(proj_root_directory):
            for file in files:
                name, extension = os.path.splitext(file)
                if extension in ['.cpp', '.cc', '.cxx', '.c', '.h', '.hh', '.hpp']:
                    full_path = os.path.join(dirpath, file)
                    logging.info("Indexing ... {0}".format(full_path))
                    self.parser.run(full_path, full_path, compiler_args, proj_root_directory)

        logging.info("Indexing for {0} completed.".format(proj_root_directory))

    def __save_to_disk(self, args):
        # TODO: Serialize AST's into the file so we can recover once we reload the project
        pass

    def __load_from_disk(self, args):
        pass

    def __go_to_definition(self, args):
        cursor = self.parser.get_definition(str(args[0]), str(args[1]), int(args[2]), int(args[3]))
        if cursor:
            logging.info("go_to_definition() location %s" % str(cursor.location))

        if self.callback:
            self.callback.go_to_definition(cursor, args)
