import os
from services.indexer.symbol_database import SymbolDatabase

class GoToDefinition():
    def __init__(self, parser, symbol_db, callback = None):
        self.parser = parser
        self.symbol_db = symbol_db
        self.callback = callback

    def __call__(self, proj_root_directory, compiler_args, args):
        contents_filename = str(args[0])
        original_filename = str(args[1])
        line              = int(args[2])
        column            = int(args[3])

        if self.callback:
            def_filename, def_line, def_column = '', 0, 0
            cursor = self.parser.get_cursor(
                        self.parser.parse(
                            contents_filename, original_filename,
                            compiler_args, proj_root_directory
                        ),
                        line, column
                    )
            definition = self.parser.get_definition(cursor)

            # If unsuccessful, try once more by extracting the definition from indexed symbol database
            if not definition:
                definition = self.symbol_db.get_definition(
                                cursor.referenced.get_usr() if cursor.referenced else cursor.get_usr(),
                             ).fetchall()
                if definition:
                    def_filename, def_line, def_column = definition[0][0], definition[0][2], definition[0][3]
            else:
                loc = definition.location
                def_filename, def_line, def_column = loc.file.name, loc.line, loc.column

            # If we are currently editing the file and our resulting cursor is exactly in that file,
            # then we should be reporting original filename instead of the temporary one.
            # That makes it possible to jump to definitions in edited (and not yet saved) files.
            if contents_filename != original_filename:
                if def_filename == contents_filename:
                    def_filename = original_filename

            self.callback([def_filename, def_line, def_column])

# TODO
#       2. Change DB schema columns order (i.e. filename, line, column, context, usr, is_definition)
#       3. ?
