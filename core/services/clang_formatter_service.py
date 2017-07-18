import logging
import subprocess
from services.yavide_service import YavideService
from common.yavide_utils import YavideUtils

class ClangSourceCodeFormatter(YavideService):
    def __init__(self, server_queue, yavide_instance):
        YavideService.__init__(self, server_queue, yavide_instance, self.__startup_hook)
        self.config_file = ""
        self.format_cmd = "clang-format -i -style=file -assume-filename="

    def __startup_hook(self, config_file):
        self.config_file = config_file
        self.format_cmd += self.config_file
        logging.info("Config_file = {0}. Format_cmd = {1}".format(self.config_file, self.format_cmd))

    def __call__(self, filename):
        cmd = self.format_cmd + " " + filename
        ret = subprocess.call(cmd, shell=True)
        logging.info("Filename = {0}. Cmd = {1}".format(filename, cmd))
        YavideUtils.call_vim_remote_function(self.yavide_instance, "Y_SrcCodeFormatter_Apply('" + filename + "')")

