import sys
import argparse
import logging
import subprocess
import tempfile
import time
from common.yavide_utils import YavideUtils
from syntax.syntax_highlighter.syntax_highlighter import VimSyntaxHighlighter
from syntax.syntax_highlighter.tag_identifier import TagIdentifier
from multiprocessing import Process, Queue

class Service():
    def __init__(self, server_queue, yavide_instance):
        self.queue = Queue()
        self.server_queue = server_queue
        self.yavide_instance = yavide_instance
        self.action = {
            0x0 : self.startup_impl,
            0x1 : self.shutdown_impl,
            0x2 : self.run_impl
        }
        self.exit_main_loop = False
        logging.info("Yavide instance: {0}".format(self.yavide_instance))
        logging.info("Actions: {0}".format(self.action))

    def startup_impl(self, payload):
        logging.info("Service startup ... Payload = {0}".format(payload))
        return self.startup_hook(payload)

    def startup_hook(self, payload):
        logging.info("Default service startup hook. Payload = {0}".format(payload))
        return

    def shutdown_impl(self, payload):
        logging.info("Service shutdown ... Payload = {0}".format(payload))
        self.exit_main_loop = True
        self.shutdown_hook(payload)

    def shutdown_hook(self, payload):
        logging.info("Default service shutdown hook. Payload = {0}".format(payload))
        return

    def run_impl(self, payload):
        logging.info("Default service run impl. Payload = {0}".format(payload))
        return

    def unknown_action(self, payload):
        logging.error("Unknown action triggered! Valid actions are: {0}".format(self.action))
        return

    def run(self):
        while self.exit_main_loop is False:
            logging.info("Listening on a request ...")
            payload = self.queue.get()
            logging.info("Request received. Payload = {0}".format(payload))
            self.action.get(payload[0], self.unknown_action)(payload[1])
        logging.info("Yavide service shut down.")

    def put_msg(self, payload):
        self.queue.put(payload)

class ClangSourceCodeFormatter(Service):
    def __init__(self, server_queue, yavide_instance):
        Service.__init__(self, server_queue, yavide_instance)
        self.config_file = ""

    def startup_hook(self, config_file):
        self.config_file = config_file
        self.format_cmd = "clang-format -i -style=" + self.config_file
        logging.info("Config_file = {0}. Format_cmd = {1}".format(self.config_file, self.format_cmd))

    def run_impl(self, filename):
        filename = filename
        cmd = self.format_cmd + " " + filename
        ret = subprocess.call(cmd, shell=True)
        logging.info("Filename = {0}. Cmd = {1}".format(filename, cmd))
        YavideUtils.call_vim_remote_function(self.yavide_instance, "Y_SrcCodeFormatter_Apply('" + filename + "')")

class ProjectBuilder(Service):
    def __init__(self, server_queue, yavide_instance):
        Service.__init__(self, server_queue, yavide_instance)
        self.build_cmd_dir = ""
        self.build_cmd = ""

    def startup_hook(self, args):
        self.build_cmd_dir = args[0]
        self.build_cmd = args[1]
        self.build_cmd_output_file = tempfile.NamedTemporaryFile(prefix='yavide', suffix='build', delete=True)
        logging.info("Args = {0}, build_cmd_output_file = {1}.".format(args, self.build_cmd_output_file.name))

    def run_impl(self, arg):
        start = time.clock()
        self.build_cmd_output_file.truncate()
        cmd = "cd " + self.build_cmd_dir + " && " + self.build_cmd
        ret = subprocess.call(cmd, shell=True, stdout=self.build_cmd_output_file, stderr=self.build_cmd_output_file)
        end = time.clock()
        logging.info("Cmd '{0}' took {1}".format(cmd, end-start))
        YavideUtils.call_vim_remote_function(self.yavide_instance, "Y_ProjectBuilder_Apply('" + self.build_cmd_output_file.name + "')")

class SourceCodeHighlighter(Service):
    def __init__(self, server_queue, yavide_instance):
        Service.__init__(self, server_queue, yavide_instance)
        self.output_directory = "/tmp"
        self.tag_id_list = [
            TagIdentifier.getClassId(),
            TagIdentifier.getClassStructUnionMemberId(),
            TagIdentifier.getEnumId(),
            TagIdentifier.getEnumValueId(),
            TagIdentifier.getExternFwdDeclarationId(),
            TagIdentifier.getFunctionDefinitionId(),
            TagIdentifier.getFunctionPrototypeId(),
            TagIdentifier.getLocalVariableId(),
            TagIdentifier.getMacroId(),
            TagIdentifier.getNamespaceId(),
            TagIdentifier.getStructId(),
            TagIdentifier.getTypedefId(),
            TagIdentifier.getUnionId(),
            TagIdentifier.getVariableDefinitionId()
        ]
        self.syntax_highlighter = VimSyntaxHighlighter(self.tag_id_list, self.output_directory)
        logging.info("tag_id_list = {0}.".format(self.tag_id_list))

    def run_impl(self, filename):
        start = time.clock()
        self.syntax_highlighter.generate_vim_syntax_file(filename)
        end = time.clock()
        logging.info("Generating vim syntax for '{0}' took {1}.".format(filename, end-start))
        YavideUtils.call_vim_remote_function(self.yavide_instance, "Y_CodeHighlight_Apply('" + filename + "')")

class YavideServer():
    def __init__(self, msg_queue, yavide_instance):
        self.msg_queue = msg_queue
        self.yavide_instance = yavide_instance
        self.service = {
            0x0 : SourceCodeHighlighter(self.msg_queue, self.yavide_instance),
            0x1 : ProjectBuilder(self.msg_queue, self.yavide_instance),
            0x2 : ClangSourceCodeFormatter(self.msg_queue, self.yavide_instance)
        }
        self.service_processes = {}
        self.action = {
            0xF0 : self.start_all_services,
            0xF1 : self.start_service,
            0xF2 : self.run_service,
            0xFD : self.shutdown_all_services,
            0xFE : self.shutdown_service,
            0xFF : self.shutdown_and_exit
        }
        self.exit_main_loop = False
        logging.info("Yavide instance: {0}".format(self.yavide_instance))
        logging.info("Registered services: {0}".format(self.service))
        logging.info("Actions: {0}".format(self.action))

    def start_all_services(self, dummyServiceId, dummyPayload):
        logging.info("Starting all registered services ... {0}".format(self.service))
        for id, svc in self.service.iteritems():
            p = Process(target=svc.run)
            p.daemon = False
            p.start()
            self.service_processes[id] = p
            self.service[id].put_msg([0x0, "start_service"])

    def start_service(self, serviceId, payload):
        logging.info("Starting the service with serviceId = {0}. Payload = {1}".format(serviceId, payload))
        if serviceId in self.service:
            p = Process(target=self.service[serviceId].run)
            p.daemon = False
            p.start()
            self.service_processes[serviceId] = p
            self.service[serviceId].put_msg([0x0, payload])
        else:
            logging.error("No service found with serviceId = {0}.".format(serviceId))

    def shutdown_all_services(self, dummyServiceId, dummyPayload):
        logging.info("Shutting down all registered services ... {0}".format(self.service))
        if self.service_processes:
            for id, svc in self.service.iteritems():
                svc.put_msg([0x1, "shutdown_service"])
            for svc_id, svc_process in self.service_processes.iteritems():
                svc_process.join()
            self.service_processes = {}

    def shutdown_service(self, serviceId, payload):
        logging.info("Shutting down the service with serviceId = {0}. Payload = {1}".format(serviceId, payload))
        if serviceId in self.service:
            self.service[serviceId].put_msg([0x1, "shutdown_service"])
            self.service_processes[serviceId].join()
            del self.service_processes[serviceId]
        else:
            logging.error("No service found with serviceId = {0}.".format(serviceId))

    def shutdown_and_exit(self, dummyServiceId, dummyPayload):
        logging.info("Shutting down the Yavide server ...")
        self.shutdown_all_services(dummyServiceId, dummyPayload)
        self.exit_main_loop = True

    def run_service(self, serviceId, payload):
        logging.info("Triggering service with serviceId = {0}. Payload = {1}".format(serviceId, payload))
        if serviceId in self.service:
            self.service[serviceId].put_msg([0x2, payload])
        else:
            logging.error("No service found with serviceId = {0}.".format(serviceId))

    def unknown_action(self, serviceId, payload):
        logging.error("Unknown action triggered! Valid actions are: {0}".format(self.action))
        return

    def run(self):
        while self.exit_main_loop is False:
            logging.info("Listening on a request ...")
            payload = self.msg_queue.get()
            logging.info("Request received. Payload = {0}".format(payload))
            self.action.get(int(payload[0]), self.unknown_action)(int(payload[1]), payload[2])
        logging.info("Yavide server shut down.")

def yavide_server_run(msg_queue, yavide_instance):
    FORMAT = '[%(levelname)s] [%(filename)s:%(lineno)s] %(funcName)25s(): %(message)s'
    yavide_server_log = tempfile.gettempdir() + '/' + yavide_instance + '_server.log'
    logging.basicConfig(filename=yavide_server_log, filemode='w', format=FORMAT, level=logging.INFO)
    logging.info('Starting a Yavide server ...')
    YavideServer(msg_queue, yavide_instance).run()

def main():
    q = Queue()
    #q.put([0xF0, "start_all_services"])
    q.put([0xF1, 0, "--class --struct --func"])
    q.put([0xF1, 1, ["/home/vagrant/repositories/navi_development/nav_business_ctrl", "./build.sh"]])
    q.put([0xF1, 2, "/home/vagrant/repositories/navi_development/nav_business_ctrl/.clang_format"])
    q.put([0xF2, 0, "/home/vagrant/repositories/navi_development/nav_business_ctrl/src/datastore/src/navctrl/datastore/Dataset.cpp"])
    q.put([0xF2, 2, "/home/vagrant/repositories/navi_development/nav_business_ctrl/src/datastore/src/navctrl/datastore/Dataset.cpp"])
    q.put([0xFF, 0, "shutdown_and_exit"])
    yavide_server_run(q, "YAVIDE1")

if __name__ == "__main__":
    main()

