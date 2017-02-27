class TypeDeduction():
    def __init__(self, parser, callback = None):
        self.parser = parser
        self.callback = callback

    def __call__(self, args):
        filename = str(args[0])
        line = int(args[1])
        col = int(args[2])
        cursor = self.parser.map_source_location_to_cursor(filename, line, col)

        if self.callback and cursor and cursor.type:
            self.callback(cursor.type.spelling, args)
