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
                # If we are currently editing the file and our resulting cursor is exactly in that file,
                # then we should be reporting original filename instead of the temporary one.
                # That makes it possible to jump to definitions in edited (and not yet saved) files.
                if contents_filename != original_filename:
                    if cursor.location.file.name == contents_filename:
                        filename = original_filename
                    else:
                        filename = cursor.location.file.name
                else:
                    filename = cursor.location.file.name
                self.callback([filename, cursor.location.line, cursor.location.column, cursor.location.offset])
            else:
                self.callback(['', 0, 0, 0])

