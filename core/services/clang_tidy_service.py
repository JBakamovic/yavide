import logging
import os
import subprocess
import tempfile
import time
from services.yavide_service import YavideService
from common.yavide_utils import YavideUtils

class ClangTidy(YavideService):
    def __init__(self, yavide_instance, request_callback):
        YavideService.__init__(self, yavide_instance, self.__startup_callback, self.__shutdown_callback, request_callback)
        self.config_file = ''
        self.output_file = tempfile.NamedTemporaryFile(prefix=self.yavide_instance, suffix='_clang_tidy_output')
        self.compiler_options = ''
        self.cmd = 'clang-tidy'

    def __startup_callback(self, args):
        self.config_file = args[0]
        compilation_database = args[1]
        root, ext = os.path.splitext(compilation_database)
        if ext == '.json':  # In case we have a JSON compilation database we simply use one
            self.compiler_options = '-p ' + compilation_database
            logging.info("clang-tidy will extract compiler flags from existing JSON database.")
        else:               # Otherwise we provide compilation flags inline
            with open(compilation_database) as f:
                self.compiler_options = '-- ' + f.read().replace('\n', ' ')
            logging.info("clang-tidy will use compiler flags given inline: '{0}'.".format(self.compiler_options))
        YavideUtils.call_vim_remote_function(self.yavide_instance, "Y_ClangTidy_StartCompleted()")

    def __shutdown_callback(self, args):
        reply_with_callback = bool(args)
        if reply_with_callback:
            YavideUtils.call_vim_remote_function(self.yavide_instance, "Y_ClangTidy_StopCompleted()")

    def __call__(self, args):
        filename, apply_fixes = args
        cmd = self.cmd + ' ' + filename + ' ' + str('-fix' if apply_fixes else '') + ' ' + self.compiler_options
        logging.info("Triggering clang-tidy over '{0}' with '{1}'".format(filename, cmd))
        with open(self.output_file.name, 'w') as f:
            start = time.clock()
            ret = subprocess.call(cmd, shell=True, stdout=f)
            end = time.clock()
        logging.info("Clang-Tidy over '{0}' completed in {1}s.".format(filename, end-start))
        return ret, self.output_file.name
