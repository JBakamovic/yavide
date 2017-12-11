class SyntaxHighlighter():
    def __init__(self, parser):
        self.parser = parser

    def __call__(self, args):
        contents_filename = str(args[0])
        original_filename = str(args[1])

        tunit = self.parser.parse(contents_filename, original_filename)
        return tunit != None, [tunit, self.parser]
