import logging
from common.yavide_utils import YavideUtils

class TypeDeduction():
    def __init__(self, parser, callback = None):
        self.parser = parser
        self.callback = callback

    def __call__(self, args):
        original_filename = str(args[0])
        contents_filename = str(args[1])
        line = int(args[2])
        col = int(args[3])
        type_spelling = self.parser.map_source_location_to_type(original_filename, contents_filename, line, col)

        if self.callback:
            self.callback(type_spelling, args)

