import logging
import time

class SyntaxHighlighter():
    def __init__(self, parser, callback = None):
        self.parser = parser
        self.callback = callback

    def __call__(self, args):
        project_root_directory = str(args[0])
        contents_filename = str(args[1])
        original_filename = str(args[2])
        compiler_args = str(args[3])

        if self.callback:
            self.callback(
                self.parser.parse(
                    contents_filename,
                    original_filename,
                    compiler_args,
                    project_root_directory
                ),
                self.parser,
                args
            )
