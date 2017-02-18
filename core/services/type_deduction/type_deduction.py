class TypeDeduction():
    def __init__(self, parser, callback = None):
        self.parser = parser
        self.callback = callback

    def __call__(self, args):
        contents_filename = str(args[0])
        original_filename = str(args[1])
        line              = int(args[2])
        column            = int(args[3])

        if self.callback:
            tunit  = self.parser.parse(contents_filename, original_filename)
            cursor = self.parser.get_cursor(tunit, line, column)
            if cursor and cursor.type:
                self.callback(cursor.type.spelling, args)
            else:
                self.callback('', args)

