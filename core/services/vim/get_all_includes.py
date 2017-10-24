import logging
from common.yavide_utils import YavideUtils

class VimGetAllIncludes():
    def __init__(self, yavide_instance):
        self.yavide_instance = yavide_instance

    def __call__(self, includes_iterator, args):
        includes = []
        if includes_iterator:
            for include in includes_iterator:
                if include.depth != -1:
                    includes.append(
                        "{'filename': '" + str(args[1]) + "', " +
                        "'lnum': '" + str(include.location.line) + "', " +
                        "'col': '" + str(include.location.column) + "', " +
                        "'type': 'I', " +
                        "'text': 'depth=" + str(include.depth) + " | src=" + str(include.source.name) + " | tgt=" + str(include.include.name) + "'}"
                    )

        YavideUtils.call_vim_remote_function(self.yavide_instance, "Y_SrcCodeGetAllIncludes_Apply(" + str(includes).replace('"', r"") + ")")
        logging.info("includes = " + str(includes).replace('"', r""))

