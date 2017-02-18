import logging
from common.yavide_utils import YavideUtils

class VimGoToDefinition():
    def __init__(self, yavide_instance):
        self.yavide_instance = yavide_instance

    def __call__(self, args):
        filename, line, column = args
        YavideUtils.call_vim_remote_function(self.yavide_instance, "Y_SrcCodeNavigation_GoToDefinitionCompleted('" + filename + "', " + str(line) + ", " + str(column) + ")")
        logging.info('Definition found at {0} [{1}, {2}]'.format(filename, line, column))
