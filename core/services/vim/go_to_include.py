import logging
from common.yavide_utils import YavideUtils

class VimGoToInclude():
    def __init__(self, yavide_instance):
        self.yavide_instance = yavide_instance

    def __call__(self, include, args):
        YavideUtils.call_vim_remote_function(self.yavide_instance, "Y_SrcCodeNavigation_GoToIncludeCompleted('" + str(include) + "')")
        logging.info("include filename = " + str(include))
