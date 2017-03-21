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

    def __unknown_op(self, args):
        logging.error("Unknown operation triggered! Valid operations are: {0}".format(self.op))

    def __load_from_disk(self, args):
        start = time.clock()
        success = self.parser.load_from_disk(str(args[0]))
        time_elapsed = time.clock() - start
        logging.info("Loading from {0} took {1}.".format(str(args[0]), time_elapsed))

        if self.callback:
            self.callback(0x0, success)

    def __save_to_disk(self, args):
        start = time.clock()
        success = self.parser.save_to_disk(str(args[0]))
        time_elapsed = time.clock() - start
        logging.info("Saving to {0} took {1}.".format(str(args[0]), time_elapsed))

        if self.callback:
            self.callback(0x1, success)

    def __run_on_single_file(self, args):
        proj_root_directory = str(args[0])
        contents_filename = str(args[1])
        original_filename = str(args[2])
        compiler_args = str(args[3])
        logging.info("Indexing a single file '{0}' ... ".format(original_filename))

        # Append additional include path to the compiler args which points to the parent directory of current buffer.
        #   * This needs to be done because we will be doing analysis on temporary file which is located outside the project
        #     directory. By doing this, we might invalidate header includes for that particular file and therefore trigger
        #     unnecessary Clang parsing errors.
        #   * An alternative would be to generate tmp files in original location but that would pollute project directory and
        #     potentially would not play well with other tools (indexer, version control, etc.).
        if contents_filename != original_filename:
            compiler_args += ' -I' + os.path.dirname(original_filename)

        # TODO Run this in a separate non-blocking process
        # TODO Indexing a single file does not guarantee us we'll have up-to-date AST's
        #       * Problem:
        #           * File we are indexing might be a header which is included in another translation unit
        #           * We would need a TU dependency tree to update influenced translation units as well
        # Index a single file
        start = time.clock()
        self.parser.run(contents_filename, original_filename, list(str(compiler_args).split()), proj_root_directory)
        time_elapsed = time.clock() - start
        logging.info("Indexing {0} took {1}.".format(original_filename, time_elapsed))

        if self.callback:
            self.callback(0x2, args)

    def __run_on_directory(self, args):
        proj_root_directory = str(args[0])
        compiler_args = list(str(args[1]).split())
        logging.info("Indexing a whole project '{0}' ... ".format(proj_root_directory))

        # TODO High RAM consumption:
        #        1. After successful completion, RAM usage stays quite high (5GB for cppcheck)
        #        2. But when we load results on load_from_disk(), RAM usage is marginally lower!
        #      Valgrind does not report _any_ memory leaks for the 1st case as
        #      one may have expected. It only reports 'still reachable' blocks but whose size
        #      is nowhere near to the
        #      occupied RAM (MBs vs GBs). This implies that parse()'ing all over
        #      and over again results in small runtime artifacts consuming
        # TODO Utilize malloc_trim(0) to swap the memory back to the OS
        # TODO Run this in a separate non-blocking process
        # TODO Run indexing of each file in separate (parallel) jobs to make it faster?
        # Index each file in project root directory
        start = time.clock()
        self.parser.drop_all_translation_units()
        for dirpath, dirs, files in os.walk(proj_root_directory):
            for file in files:
                name, extension = os.path.splitext(file)
                if extension in ['.cpp', '.cc', '.cxx', '.c', '.h', '.hh', '.hpp']:
                    full_path = os.path.join(dirpath, file)
                    logging.info("Indexing ... {0}".format(full_path))
                    self.parser.run(full_path, full_path, compiler_args, proj_root_directory)
        time_elapsed = time.clock() - start
        logging.info("Indexing {0} took {1}.".format(proj_root_directory, time_elapsed))

        if self.callback:
            self.callback(0x3, args)

    def __drop_single_file(self, args):
        self.parser.drop_translation_unit(str(args[0]))
        if self.callback:
            self.callback(0x4, args)

    def __drop_all(self, dummy = None):
        self.parser.drop_all_translation_units()
        if self.callback:
            self.callback(0x5, dummy)

    def __go_to_definition(self, args):
        cursor = self.parser.get_definition(str(args[0]), int(args[1]), int(args[2]))
        if cursor:
            logging.info('Definition location %s' % str(cursor.location))
        else:
            logging.info('No definition found.')

        if self.callback:
            self.callback(0x10, cursor.location if cursor else None)

    def __find_all_references(self, args):
        start = time.clock()
        references = self.parser.find_all_references(str(args[0]), int(args[1]), int(args[2]))
        time_elapsed = time.clock() - start
        logging.info("Find all references of [{0}, {1}] in {2} took {3}.".format(args[1], args[2], args[0], time_elapsed))
        for r in references:
            logging.info("Ref location %s" % str(r))

        if self.callback:
            self.callback(0x11, references)
