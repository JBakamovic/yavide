import logging
from common.yavide_utils import YavideUtils

class TypeDeduction():
    def __init__(self, parser, callback = None):
        self.parser = parser
        self.callback = callback

    def __call__(self, args):
        filename = str(args[0])
        line = int(args[1])
        col = int(args[2])
        type_spelling = self.parser.map_source_location_to_type(filename, line, col)

        if self.callback:
            self.callback(type_spelling, args)

