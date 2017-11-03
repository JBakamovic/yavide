import logging
from common.yavide_utils import YavideUtils

class VimGetAllIncludes():
    def __init__(self, yavide_instance):
        self.yavide_instance = yavide_instance

    def __call__(self, includes_iterator, args):
        includes = []
        for include in includes_iterator:
            includes.append(
                "{'filename': '" + str(args[1]) + "', " +
                "'lnum': '" + str(include.location.line) + "', " +
                "'col': '" + str(include.location.column) + "', " +
                "'type': 'I', " +
                "'text': 'depth=" + str(include.depth) + " | src=" + str(include.source.name) + " | tgt=" + str(include.include.name) + "'}"
            )

        #includes = []
        #for include in includes_iterator:
        #    includes.append(
        #        "{'filename': '" + str(args[1]) + "', " +
        #        "'lnum': '" + str(include[1]) + "', " +
        #        "'col': '" + str(include[2]) + "', " +
        #        "'type': 'I', " +
        #        "'text': '" + str(include[0]) + "'}"
        #    )

        YavideUtils.call_vim_remote_function(self.yavide_instance, "Y_SrcCodeGetAllIncludes_Apply(" + str(includes).replace('"', r"") + ")")
        logging.info("includes = " + str(includes).replace('"', r""))

