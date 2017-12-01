import logging
import subprocess
from services.yavide_service import YavideService
from common.yavide_utils import YavideUtils

class ClangTidy(YavideService):
    def __init__(self, yavide_instance):
        YavideService.__init__(self, yavide_instance, self.__startup_callback, self.__shutdown_callback)
        self.config_file = ""
        self.compiler_options = ""
        self.cmd = "clang-tidy "

    def __startup_callback(self, args):
        self.config_file = args[0]
        compilation_database = args[1]
        root, ext = os.path.splitext(self.compilation_database)
        if ext == '.json':
            self.compiler_options = '-p ' + compilation_database # we simply use the JSON database
        else:
            compile_flags = [line.rstrip('\n') for line in open(compilation_database)]
            self.cmd += '-- ' + compile_flags # otherwise we provide compilation flags inline

        YavideUtils.call_vim_remote_function(self.yavide_instance, "Y_ClangTidy_StartCompleted()")
        logging.info("Config_file = {0}. Format_cmd = {1}".format(self.config_file, self.cmd))

    def __shutdown_callback(self, args):
        reply_with_callback = bool(args)
        if reply_with_callback:
            YavideUtils.call_vim_remote_function(self.yavide_instance, "Y_ClangTidy_StopCompleted()")

    def __call__(self, filename):
        cmd = self.cmd + " " + filename
        ret = subprocess.call(cmd, shell=True)
        logging.info("Filename = {0}. Cmd = {1}".format(filename, cmd))
        YavideUtils.call_vim_remote_function(self.yavide_instance, "Y_ClangTidy_Apply('" + filename + "')")


