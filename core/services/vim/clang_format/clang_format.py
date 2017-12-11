from common.yavide_utils import YavideUtils

class VimClangFormat():
    def __init__(self, yavide_instance):
        self.yavide_instance = yavide_instance

    def __call__(self, success, args, payload):
        YavideUtils.call_vim_remote_function(self.yavide_instance, "Y_SrcCodeFormatter_Apply('" + args + "')")

