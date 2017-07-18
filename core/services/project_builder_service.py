import logging
import subprocess
import tempfile
import time
from services.yavide_service import YavideService
from common.yavide_utils import YavideUtils

class ProjectBuilder(YavideService):
    def __init__(self, server_queue, yavide_instance):
        YavideService.__init__(self, server_queue, yavide_instance, self.__startup_hook)
        self.build_cmd_dir = ""
        self.build_cmd_output_file = ""

    def __startup_hook(self, args):
        self.build_cmd_dir = args[0]
        self.build_cmd_output_file = tempfile.NamedTemporaryFile(prefix='yavide', suffix='build', delete=True)
        logging.info("Args = {0}, build_cmd_output_file = {1}.".format(args, self.build_cmd_output_file.name))

    def __call__(self, arg):
        start = time.clock()
        build_cmd = arg[0]
        self.build_cmd_output_file.truncate()
        cmd = "cd " + self.build_cmd_dir + " && " + build_cmd
        ret = subprocess.call(cmd, shell=True, stdout=self.build_cmd_output_file, stderr=self.build_cmd_output_file)
        end = time.clock()
        logging.info("Cmd '{0}' took {1}".format(cmd, end-start))
        YavideUtils.call_vim_remote_function(self.yavide_instance, "Y_ProjectBuilder_Apply('" + self.build_cmd_output_file.name + "')")

