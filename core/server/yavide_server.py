import sys
import argparse
import logging
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

    def startup_impl(self, data):
        return self.startup_hook(data)

    def startup_hook(self, data):
        return

    def shutdown_impl(self, data):
        self.exit_main_loop = True
        self.shutdown_hook(data)

    def shutdown_hook(self, data):
        return

    def run_impl(self, data):
        return

    def unknown_action(self, data):
        return

    def run(self):
        while self.exit_main_loop is False:
            payload = self.queue.get()
            self.action.get(payload[0], self.unknown_action)(payload[1])

    def put_msg(self, payload):
        self.queue.put(payload)

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

    def run_impl(self, filename):
        self.syntax_highlighter.generate_vim_syntax_file(filename)
        YavideUtils.call_vim_remote_function(self.yavide_instance, "Y_CodeHighlight_Apply('" + filename + "')")

class YavideServer():
    def __init__(self, msg_queue, yavide_instance):
        self.msg_queue = msg_queue
        self.yavide_instance = yavide_instance
        self.service = {
            0x0 : SourceCodeHighlighter(self.msg_queue, self.yavide_instance)
        }
        self.service_processes = {}
        self.action_id = {
            0xF0 : self.start_all_services,
            0xF1 : self.start_service,
            0xF2 : self.shutdown_all_services,
            0xF3 : self.shutdown_service,
            0xFF : self.shutdown_and_exit
        }
        self.exit_main_loop = False

    def start_all_services(self, dummyServiceId, payload):
        for id, svc in self.service.iteritems():
            p = Process(target=svc.run)
            p.daemon = False
            p.start()
            self.service_processes[id] = p
            self.service[id].put_msg([0x0, "start_service"])

    def start_service(self, serviceId, payload):
        if self.service.has_key(serviceId):
            p = Process(target=self.service[serviceId].run)
            p.daemon = False
            p.start()
            self.service_processes[serviceId] = p
            self.service[serviceId].put_msg([0x0, "start_service"])

    def shutdown_all_services(self, dummyServiceId, payload):
        if self.service_processes:
            for id, svc in self.service.iteritems():
                svc.put_msg([0x1, "shutdown_service"])
            for svc_id, svc_process in self.service_processes.iteritems():
                svc_process.join()
            self.service_processes = {}

    def shutdown_service(self, serviceId, payload):
        if self.service.has_key(serviceId):
            self.service[serviceId].put_msg([0x1, "shutdown_service"])
            self.service_processes[serviceId].join()
            del self.service_processes[serviceId]

    def shutdown_and_exit(self, serviceId, payload):
        YavideUtils.send_vim_remote_command(self.yavide_instance, ":echomsg 'Shutdown and exit ...'")
        self.shutdown_all_services(serviceId, payload)
        self.exit_main_loop = True

    def run_service(self, serviceId, payload):
        YavideUtils.send_vim_remote_command(self.yavide_instance, ":echomsg 'run_service'")
        YavideUtils.send_vim_remote_command(self.yavide_instance, ":echomsg 'serviceId = " + str(serviceId) + "'")
        YavideUtils.send_vim_remote_command(self.yavide_instance, ":echomsg 'payload = " + payload + "'")
        if self.service.has_key(serviceId):
            YavideUtils.send_vim_remote_command(self.yavide_instance, ":echomsg 'run_service ... second time'")        
            self.service[serviceId].put_msg([0x2, payload])

    def run(self):
        while self.exit_main_loop is False:
            YavideUtils.send_vim_remote_command(self.yavide_instance, ":echomsg 'Waiting for a message ...'")
            payload = self.msg_queue.get()
            YavideUtils.send_vim_remote_command(self.yavide_instance, ":echomsg 'payload = " + payload[1] + "'")
            self.action_id.get(payload[0], self.run_service)(payload[0], payload[1])
        YavideUtils.send_vim_remote_command(self.yavide_instance, ":echomsg 'Exited main loop ...'")

def yavide_server_run(msg_queue, yavide_instance):
    YavideServer(msg_queue, yavide_instance).run()

def main():
    q = Queue()
    q.put([0xF0, "start_all_services"])
    q.put([0x0,  "test payload"])
    q.put([0xFF, "shutdown_and_exit"])
    yavide_server_run(q, "YAVIDE")

if __name__ == "__main__":
    main()

