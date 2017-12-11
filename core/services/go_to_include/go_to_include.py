class GoToInclude():
    def __init__(self, parser):
        self.parser = parser

    def __call__(self, args):
        contents_filename = str(args[0])
        original_filename = str(args[1])
        line              = int(args[2])

        include_filename = ''
        tunit = self.parser.parse(contents_filename, original_filename)
        for include in self.parser.get_top_level_includes(tunit):
            filename, l, col = include
            if l == line:
                include_filename = filename
                break
        return (tunit != None and include_filename != ''), include_filename
