import logging
from common.yavide_utils import YavideUtils

class VimTypeDeduction():
    def __init__(self, yavide_instance):
        self.yavide_instance = yavide_instance

    def __call__(self, success, type_spelling, payload):
        YavideUtils.call_vim_remote_function(self.yavide_instance, "Y_SrcCodeTypeDeduction_Apply('" + str(type_spelling) + "')")
        logging.debug("type_spelling = " + str(type_spelling))

