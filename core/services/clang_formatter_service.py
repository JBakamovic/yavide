import logging
import subprocess
from services.yavide_service import YavideService
from common.yavide_utils import YavideUtils

class ClangSourceCodeFormatter(YavideService):
    def __init__(self, yavide_instance, request_callback):
        YavideService.__init__(self, yavide_instance, self.__startup_callback, self.__shutdown_callback, request_callback)
        self.config_file = ""
        self.format_cmd = "clang-format -i -style=file -assume-filename="

    def __startup_callback(self, args):
        self.config_file = args
        self.format_cmd += self.config_file
        YavideUtils.call_vim_remote_function(self.yavide_instance, "Y_SrcCodeFormatter_StartCompleted()")
        logging.info("Config_file = {0}. Format_cmd = {1}".format(self.config_file, self.format_cmd))

    def __shutdown_callback(self, args):
        reply_with_callback = bool(args)
        if reply_with_callback:
            YavideUtils.call_vim_remote_function(self.yavide_instance, "Y_SrcCodeFormatter_StopCompleted()")

    def __call__(self, filename):
        cmd = self.format_cmd + " " + filename
        ret = subprocess.call(cmd, shell=True)
        logging.info("Filename = {0}. Cmd = {1}".format(filename, cmd))
        return ret, filename

