import logging
import os
import subprocess
import tempfile
from services.yavide_service import YavideService
from common.yavide_utils import YavideUtils

class ClangTidy(YavideService):
    def __init__(self, yavide_instance):
        YavideService.__init__(self, yavide_instance, self.__startup_callback, self.__shutdown_callback)
        self.config_file = ''
        self.output_file = tempfile.NamedTemporaryFile(prefix=self.yavide_instance, suffix='_clang_tidy_output')
        self.compiler_options = ''
        self.apply_fixes = False
        self.cmd = 'clang-tidy'

    def __startup_callback(self, args):
        self.config_file = args[0]
        compilation_database = args[1]
        self.apply_fixes = bool(args[2])
        root, ext = os.path.splitext(compilation_database)
        if ext == '.json':  # In case we have a JSON compilation database we simply use one
            self.compiler_options = '-p ' + compilation_database
            logging.info("Clang-Tidy compiler arguments configured with JSON database. Fixes will be applied automatically = '{0}'".format(str(self.apply_fixes)))
        else:               # Otherwise we provide compilation flags inline
            with open(compilation_database) as f:
                self.compiler_options = '-- ' + f.read().replace('\n', ' ')
            logging.info("Clang-Tidy compiler arguments configured inline with '{0}'. Fixes will be applied automatically = '{1}'".format(self.compiler_options, str(self.apply_fixes)))
        YavideUtils.call_vim_remote_function(self.yavide_instance, "Y_ClangTidy_StartCompleted()")

    def __shutdown_callback(self, args):
        reply_with_callback = bool(args)
        if reply_with_callback:
            YavideUtils.call_vim_remote_function(self.yavide_instance, "Y_ClangTidy_StopCompleted()")

    def __call__(self, filename):
        cmd = self.cmd + ' ' + filename + ' ' + str('-fix' if self.apply_fixes else '') + ' ' + self.compiler_options
        with open(self.output_file.name, 'w') as f:
            subprocess.call(cmd, shell=True, stdout=f)
        logging.info("Clang-Tidy over '{0}' completed with '{1}'".format(filename, cmd))
        YavideUtils.call_vim_remote_function(self.yavide_instance, "Y_ClangTidy_Apply('" + self.output_file.name + "')")

