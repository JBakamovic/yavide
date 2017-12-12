import logging
import subprocess
from services.service import Service

class ClangSourceCodeFormatter(Service):
    def __init__(self, service_plugin):
        Service.__init__(self, service_plugin)
        self.config_file = ""
        self.format_cmd = "clang-format -i -style=file -assume-filename="

    def startup_callback(self, args):
        self.config_file = args
        self.format_cmd += self.config_file
        logging.info("Config_file = {0}. Format_cmd = {1}".format(self.config_file, self.format_cmd))

    def shutdown_callback(self, args):
        pass

    def __call__(self, filename):
        cmd = self.format_cmd + " " + filename
        ret = subprocess.call(cmd, shell=True)
        logging.info("Filename = {0}. Cmd = {1}".format(filename, cmd))
        return ret, filename

