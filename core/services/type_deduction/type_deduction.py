class TypeDeduction():
    def __init__(self, tunit_pool, parser, callback = None):
        self.tunit_pool = tunit_pool
        self.parser = parser
        self.callback = callback

    def __call__(self, args):
        cursor = self.parser.map_source_location_to_cursor(self.tunit_pool[str(args[0])], int(args[1]), int(args[2]))
        if self.callback and cursor and cursor.type:
            self.callback(cursor.type.spelling, args)
