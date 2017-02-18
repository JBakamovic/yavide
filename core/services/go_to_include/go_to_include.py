class GoToInclude():
    def __init__(self, parser, callback = None):
        self.parser = parser
        self.callback = callback

    def __call__(self, args):
        contents_filename = str(args[0])
        original_filename = str(args[1])
        line              = int(args[2])

        if self.callback:
            include_filename = ''
            tunit = self.parser.parse(contents_filename, original_filename)
            for include in self.parser.get_top_level_includes(tunit):
                filename, l, col = include
                if l == line:
                    include_filename = filename
                    break

            self.callback(
                include_filename,
                args
            )
