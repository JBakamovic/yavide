class Diagnostics():
    def __init__(self, parser, callback = None):
        self.parser = parser
        self.callback = callback

    def __call__(self, args):
        contents_filename = str(args[0])
        original_filename = str(args[1])

        if self.callback:
            self.callback(
                self.parser.get_diagnostics(
                    self.parser.parse(contents_filename, original_filename)
                ),
                args
            )

