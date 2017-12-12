import logging
from multiprocessing import Process, Queue
from services.clang_formatter_service import ClangSourceCodeFormatter
from services.clang_tidy_service import ClangTidy
from services.project_builder_service import ProjectBuilder
from services.source_code_model_service import SourceCodeModel

class Server():
    def __init__(self, msg_queue, source_code_model_plugin, builder_plugin, clang_format_plugin, clang_tidy_plugin):
        self.msg_queue = msg_queue
        self.service = {
            0x0 : SourceCodeModel(source_code_model_plugin),
            0x1 : ProjectBuilder(builder_plugin),
            0x2 : ClangSourceCodeFormatter(clang_format_plugin),
            0x3 : ClangTidy(clang_tidy_plugin)
        }
        self.service_processes = {}
        self.action = {
            0xF0 : self.__start_all_services,
            0xF1 : self.__start_service,
            0xF2 : self.__send_service_request,
            0xFD : self.__shutdown_all_services,
            0xFE : self.__shutdown_service,
            0xFF : self.__shutdown_and_exit
            # TODO add runtime debugging switch action
        }
        self.keep_listening = True
        logging.info("Registered services: {0}".format(self.service))
        logging.info("Actions: {0}".format(self.action))

    def __start_all_services(self, dummyServiceId, dummyPayload):
        logging.info("Starting all registered services ... {0}".format(self.service))
        for id, svc in self.service.iteritems():
            p = Process(target=svc.listen, name=svc.__class__.__name__)
            p.daemon = False
            p.start()
            self.service_processes[id] = p
            self.service[id].send_startup_request(dummyPayload)

    def __start_service(self, serviceId, payload):
        logging.info("Starting the service with serviceId = {0}. Payload = {1}".format(serviceId, payload))
        if serviceId in self.service:
            p = Process(target=self.service[serviceId].listen)
            p.daemon = False
            p.start()
            self.service_processes[serviceId] = p
            self.service[serviceId].send_startup_request(payload)
        else:
            logging.error("No service found with serviceId = {0}.".format(serviceId))

    def __shutdown_all_services(self, dummyServiceId, payload):
        logging.info("Shutting down all registered services ... {0}".format(self.service))
        if self.service_processes:
            for id, svc in self.service.iteritems():
                svc.send_shutdown_request(payload)
            for svc_id, svc_process in self.service_processes.iteritems():
                svc_process.join()
            del self.service_processes

    def __shutdown_service(self, serviceId, payload):
        logging.info("Shutting down the service with serviceId = {0}. Payload = {1}".format(serviceId, payload))
        if serviceId in self.service:
            self.service[serviceId].send_shutdown_request(payload)
            self.service_processes[serviceId].join()
            del self.service_processes[serviceId]
        else:
            logging.error("No service found with serviceId = {0}.".format(serviceId))

    def __shutdown_and_exit(self, dummyServiceId, payload):
        logging.info("Shutting down the server ...")
        self.__shutdown_all_services(dummyServiceId, payload)
        self.keep_listening = False

    def __send_service_request(self, serviceId, payload):
        logging.info("Triggering service with serviceId = {0}. Payload = {1}".format(serviceId, payload))
        if serviceId in self.service:
            self.service[serviceId].send_request(payload)
        else:
            logging.error("No service found with serviceId = {0}.".format(serviceId))

    def __unknown_action(self, serviceId, payload):
        logging.error("Unknown action triggered! Valid actions are: {0}".format(self.action))

    def listen(self):
        while self.keep_listening is True:
            logging.info("Listening on a request ...")
            payload = self.msg_queue.get()
            logging.info("Request received. Payload = {0}".format(payload))
            self.action.get(int(payload[0]), self.__unknown_action)(int(payload[1]), payload[2])
        logging.info("Server shut down.")





def test__clang_indexer__run_on_directory():
    proj_root_dir = "/home/jbakamovic/development/projects/cppcheck"
    compiler_args = "-I./lib -I./externals/simplecpp -I./tinyxml"
    filename = "/home/jbakamovic/development/projects/cppcheck/lib/astutils.cpp"

    q = Queue()
    q.put([0xF1, 0, "dummy"])
    q.put([0xF2, 0, [0x0, 0x1, proj_root_dir, compiler_args]])   # run-on-directory
    server_run(q, 'YAVIDE_DEV')

def test__clang_indexer__find_all_references():
    proj_root_dir = "/home/jbakamovic/development/projects/cppcheck"
    compiler_args = "-I./lib -I./externals/simplecpp -I./tinyxml"
    filename = "/home/jbakamovic/development/projects/cppcheck/lib/astutils.cpp"
    line = 27
    col = 15

    q = Queue()
    q.put([0xF1, 0, "dummy"])
    q.put([0xF2, 0, [0x0, 0x1, proj_root_dir, compiler_args]])   # run-on-directory
    q.put([0xF2, 0, [0x0, 0x11, filename, line, col]])           # find-all-references
    server_run(q, 'YAVIDE_DEV')

def test__clang_syntax_highlighter():
    proj_root_dir = "/home/jbakamovic/development/projects/cppcheck"
    compiler_args = "-I./lib -I./externals/simplecpp -I./tinyxml"
    filename = "/home/jbakamovic/development/projects/cppcheck/lib/astutils.cpp"

    q = Queue()
    q.put([0xF1, 0, "dummy"])
    q.put([0xF2, 0, [0x1, proj_root_dir, filename, filename, compiler_args]]) # syntax-highlight
    server_run(q, 'YAVIDE_DEV')

def test__clang_diagnostics():
    proj_root_dir = "/home/jbakamovic/development/projects/cppcheck"
    compiler_args = "-I./lib -I./externals/simplecpp -I./tinyxml"
    filename = "/home/jbakamovic/development/projects/cppcheck/lib/astutils.cpp"

    q = Queue()
    q.put([0xF1, 0, "dummy"])
    q.put([0xF2, 0, [0x2, proj_root_dir, filename, filename, compiler_args]]) # diagnostics
    server_run(q, 'YAVIDE_DEV')

def test__clang_type_deduction():
    proj_root_dir = "/home/jbakamovic/development/projects/cppcheck"
    compiler_args = "-I./lib -I./externals/simplecpp -I./tinyxml"
    filename = "/home/jbakamovic/development/projects/cppcheck/lib/astutils.cpp"
    line = 27
    col = 15

    q = Queue()
    q.put([0xF1, 0, "dummy"])
    q.put([0xF2, 0, [0x3, proj_root_dir, filename, filename, compiler_args, line, col]]) # type-deduction
    server_run(q, 'YAVIDE_DEV')


def main():
    return test__clang_indexer__find_all_references()
    return test__clang_indexer__run_on_directory()
    return test__clang_type_deduction()
    return test__clang_diagnostics()
    return test__clang_syntax_highlighter()

    q = Queue()
    #q.put([0xF0, "start_all_services"])
    q.put([0xF1, 0, "--class --struct --func"])
    q.put([0xF1, 1, ["/home/vagrant/repositories/navi_development/nav_business_ctrl", "./build.sh"]])
    q.put([0xF1, 2, "/home/vagrant/repositories/navi_development/nav_business_ctrl/.clang_format"])
    q.put([0xF1, 3, ['4', '.cpp', '.cc', '.h', '.hh', '.hpp', '/home/vagrant/repositories/navi_development/nav_business_ctrl', '.cxx_tags', '.java_tags', 'cscope.out']])
    q.put([0xF2, 0, "/home/vagrant/repositories/navi_development/nav_business_ctrl/src/datastore/src/navctrl/datastore/Dataset.cpp"])
    q.put([0xF2, 2, "/home/vagrant/repositories/navi_development/nav_business_ctrl/src/datastore/src/navctrl/datastore/Dataset.cpp"])
    q.put([0xFF, 0, "shutdown_and_exit"])
    server_run(q, "YAVIDE1")

if __name__ == "__main__":
    main()

