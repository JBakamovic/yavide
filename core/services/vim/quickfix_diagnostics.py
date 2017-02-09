import logging
from common.yavide_utils import YavideUtils

class VimQuickFixDiagnostics():
    def __init__(self, yavide_instance):
        self.yavide_instance = yavide_instance

    def __call__(self, clang_parser, args):
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
        for d in clang_parser.get_diagnostics():
            diagnostics.append(
                "{'bufnr': '" + str(args[0]) + "', " +
                "'lnum': '" + str(d.location.line) + "', " +
                "'col': '" + str(d.location.column) + "', " +
                "'type': '" + clang_severity_to_quickfix_type(d.severity) + "', " +
                "'text': '" + d.category_name + " | " + str(d.spelling).replace("'", r"") + "'}"
            )

        YavideUtils.call_vim_remote_function(self.yavide_instance, "Y_SrcCodeDiagnostics_Apply(" + str(diagnostics).replace('"', r"") + ")")
        logging.debug("Diagnostics: " + str(diagnostics))

