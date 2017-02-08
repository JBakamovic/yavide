import logging
import time

class SyntaxHighlighter():
    def __init__(self, parser, syntax_generator):
        self.parser = parser
        self.syntax_generator = syntax_generator

    def run_impl(self, args):
        contents_filename = str(args[0])
        original_filename = str(args[1])
        compiler_args = list(str(args[2]).split())
        project_root_directory = str(args[3])
        start = time.clock()
        self.parser.run(contents_filename, original_filename, compiler_args, project_root_directory)
        parsing_time = time.clock() - start
        start = time.clock()
        self.syntax_generator.run(self.parser)
        syntax_generator_time = time.clock() - start
        logging.info("Syntax highlighting for '{0}' took {1}. Parsing {2} + syntax generator {3}.".format(original_filename, parsing_time + syntax_generator_time, parsing_time, syntax_generator_time))

