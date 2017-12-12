import logging
import os
import subprocess
import tempfile
import time
from services.yavide_service import YavideService

class ClangTidy(YavideService):
    def __init__(self, output_prefix, service_plugin):
        YavideService.__init__(self, service_plugin)
        self.config_file = ''
        self.output_file = tempfile.NamedTemporaryFile(prefix=output_prefix, suffix='_clang_tidy_output')
        self.compiler_options = ''
        self.cmd = 'clang-tidy'

    def startup_callback(self, args):
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

    def shutdown_callback(self, args):
        pass

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
