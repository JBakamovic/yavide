class TypeDeduction():
    def __init__(self, parser, callback = None):
        self.parser = parser
        self.callback = callback

    def __call__(self, proj_root_directory, args):
        contents_filename = str(args[0])
        original_filename = str(args[1])
        line = int(args[2])
        column = int(args[3])

        tunit = self.parser.parse(
            contents_filename,
            original_filename,
            proj_root_directory
        )

        if self.callback:
            cursor = self.parser.get_cursor(tunit, line, column)
            if cursor and cursor.type:
                self.callback(cursor.type.spelling, args)
            else:
                self.callback('', args)

