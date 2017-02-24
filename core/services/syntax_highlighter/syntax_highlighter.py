import logging
import time

class SyntaxHighlighter():
    def __init__(self, parser, callback = None):
        self.parser = parser
        self.callback = callback

    def __call__(self, args):
        contents_filename = str(args[0])
        original_filename = str(args[1])
        compiler_args = list(str(args[2]).split())
        project_root_directory = str(args[3])
        if contents_filename != original_filename:
            start = time.clock()
            self.parser.run(contents_filename, original_filename, compiler_args, project_root_directory)
            time_elapsed = time.clock() - start
            logging.info("Parsing '{0}' took {1}.".format(original_filename, time_elapsed))

        if self.callback:
            self.callback(self.parser, args)

