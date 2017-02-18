import logging
from common.yavide_utils import YavideUtils

class VimQuickFixDiagnostics():
    def __init__(self, yavide_instance):
        self.yavide_instance = yavide_instance

    def __call__(self, diagnostics_iter, args):
        def clang_severity_to_quickfix_type(severity):
            # Clang severity | Vim Quickfix type
            # ----------------------------------
            #   Ignored = 0     0 ()
            #   Note    = 1     I (info)
            #   Warning = 2     W (warning)
            #   Error   = 3     E (error)
            #   Fatal   = 4     other ()
            # ----------------------------------
            if severity == 0:
                return '0'
            elif severity == 1:
                return 'I'
            elif severity == 2:
                return 'W'
            elif severity == 3:
                return 'E'
            elif severity == 4:
                return 'other'
            return '0'

        diagnostics = []
        for d in diagnostics_iter:
            diagnostics.append(
                "{'bufnr': '" + str(args[1]) + "', " +
                "'lnum': '" + str(d.location.line) + "', " +
                "'col': '" + str(d.location.column) + "', " +
                "'type': '" + clang_severity_to_quickfix_type(d.severity) + "', " +
                "'text': '" + d.category_name + " | " + str(d.spelling).replace("'", r"") + "'}"
            )

            fixits = "Hint:"
            for f in d.fixits:
                fixits += \
                    " Try using '" + str(f.value) + "' instead. [col=" + \
                    str(f.range.start.column) + ":" + str(f.range.end.column) + "]"
                    # TODO How to handle multiline quickfix entries? It would be nice show each fixit in its own line.

            if len(d.fixits):
                diagnostics.append(
                    "{'bufnr': '" + str(args[1]) + "', " +
                    "'lnum': '" + str(d.location.line) + "', " +
                    "'col': '" + str(d.location.column) + "', " +
                    "'type': 'I', " +
                    "'text': '" + str(fixits).replace("'", r"") + "'}"
                )

        YavideUtils.call_vim_remote_function(self.yavide_instance, "Y_SrcCodeDiagnostics_Apply(" + str(diagnostics).replace('"', r"") + ")")
        logging.debug("Diagnostics: " + str(diagnostics))

