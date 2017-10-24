class GoToDefinition():
    def __init__(self, parser, callback = None):
        self.parser = parser
        self.callback = callback

    def __call__(self, proj_root_directory, compiler_args, args):
        contents_filename = str(args[0])
        original_filename = str(args[1])
        line              = int(args[2])
        column            = int(args[3])

        cursor = self.parser.get_definition(
            self.parser.parse(
                contents_filename,
                original_filename,
                compiler_args,
                proj_root_directory
            ),
            line, column
        )

        if self.callback:
            if cursor:
                # We still want to be able to jump to definition (in original but edited file)
                # eventhough we are operating on edited (and not saved) file
                filename = cursor.location.file.name if contents_filename == original_filename else original_filename
                self.callback([filename, cursor.location.line, cursor.location.column, cursor.location.offset])
            else:
                self.callback(['', 0, 0, 0])

