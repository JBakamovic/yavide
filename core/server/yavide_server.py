import sys
import logging
import tempfile
from multiprocessing import Process, Queue
from services.yavide_service import YavideService
from services.clang_formatter_service import ClangSourceCodeFormatter
from services.project_builder_service import ProjectBuilder
from services.indexer_service import SourceCodeIndexer
from services.syntax_highlighter_service import SyntaxHighlighter

class YavideServer():
    def __init__(self, msg_queue, yavide_instance):
        self.msg_queue = msg_queue
        self.yavide_instance = yavide_instance
        self.service = {
            0x0 : SyntaxHighlighter(self.msg_queue, self.yavide_instance),
            0x1 : ProjectBuilder(self.msg_queue, self.yavide_instance),
            0x2 : ClangSourceCodeFormatter(self.msg_queue, self.yavide_instance),
            0x3 : SourceCodeIndexer(self.msg_queue, self.yavide_instance)
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
            p = Process(target=svc.run, name=svc.__class__.__name__)
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

def handle_exception(exc_type, exc_value, exc_traceback):
    logging.critical("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))

def catch_unhandled_exceptions():
    # This is what usually should be enough
    sys.excepthook = handle_exception

    # But sys.excepthook does not work anymore within multi-threaded/multi-process environment (see https://bugs.python.org/issue1230540)
    # So what we can do is to override the YavideService.run() implementation so it includes try-catch block with exceptions
    # being forwarded to the sys.excepthook function.
    run_original = YavideService.run
    def run(self):
        try:
            run_original(self)
        except:
            sys.excepthook(*sys.exc_info())
    YavideService.run = run

def yavide_server_run(msg_queue, yavide_instance):
    # Setup catching unhandled exceptions
    catch_unhandled_exceptions()

    # Logger setup
    FORMAT = '[%(levelname)s] [%(filename)s:%(lineno)s] %(funcName)25s(): %(message)s'
    yavide_server_log = tempfile.gettempdir() + '/' + yavide_instance + '_server.log'
    logging.basicConfig(filename=yavide_server_log, filemode='w', format=FORMAT, level=logging.INFO)
    logging.info('Starting a Yavide server ...')

    # Run
    try:
        YavideServer(msg_queue, yavide_instance).run()
    except:
        sys.excepthook(*sys.exc_info())

def main():
    q = Queue()
    #q.put([0xF0, "start_all_services"])
    q.put([0xF1, 0, "--class --struct --func"])
    q.put([0xF1, 1, ["/home/vagrant/repositories/navi_development/nav_business_ctrl", "./build.sh"]])
    q.put([0xF1, 2, "/home/vagrant/repositories/navi_development/nav_business_ctrl/.clang_format"])
    q.put([0xF1, 3, ['4', '.cpp', '.cc', '.h', '.hh', '.hpp', '/home/vagrant/repositories/navi_development/nav_business_ctrl', '.cxx_tags', '.java_tags', 'cscope.out']])
    q.put([0xF2, 0, "/home/vagrant/repositories/navi_development/nav_business_ctrl/src/datastore/src/navctrl/datastore/Dataset.cpp"])
    q.put([0xF2, 2, "/home/vagrant/repositories/navi_development/nav_business_ctrl/src/datastore/src/navctrl/datastore/Dataset.cpp"])
    q.put([0xFF, 0, "shutdown_and_exit"])
    yavide_server_run(q, "YAVIDE1")

if __name__ == "__main__":
    main()

