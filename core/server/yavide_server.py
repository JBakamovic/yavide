import copy_reg
import logging
import sys
import tempfile
import types
from multiprocessing import Process, Queue
from services.yavide_service import YavideService
from services.clang_formatter_service import ClangSourceCodeFormatter
from services.project_builder_service import ProjectBuilder
from services.source_code_model_service import SourceCodeModel
from services.indexer_service import SourceCodeIndexer

def _pickle_method(method):
    func_name = method.im_func.__name__
    obj = method.im_self
    cls = method.im_class
    if func_name.startswith('__') and not func_name.endswith('__'): # Deal with 'private' functions
        cls_name = cls.__name__.lstrip('_')
        func_name = '_' + cls_name + func_name
    return _unpickle_method, (func_name, obj, cls)

def _unpickle_method(func_name, obj, cls):
    for cls in cls.__mro__:
        try:
            func = cls.__dict__[func_name]
        except KeyError:
            pass
        else:
            break
    return func.__get__(obj, cls)

# Enable pickling of class methods (required for ClangIndexer() implementation)
copy_reg.pickle(types.MethodType, _pickle_method, _unpickle_method)

class YavideServer():
    def __init__(self, msg_queue, yavide_instance):
        self.msg_queue = msg_queue
        self.yavide_instance = yavide_instance
        self.service = {
            0x0 : SourceCodeModel(self.msg_queue, self.yavide_instance),
            0x1 : ProjectBuilder(self.msg_queue, self.yavide_instance),
            0x2 : ClangSourceCodeFormatter(self.msg_queue, self.yavide_instance)
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
        logging.info("Yavide instance: {0}".format(self.yavide_instance))
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

    def __shutdown_all_services(self, dummyServiceId, dummyPayload):
        logging.info("Shutting down all registered services ... {0}".format(self.service))
        if self.service_processes:
            for id, svc in self.service.iteritems():
                svc.send_shutdown_request(dummyPayload)
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

    def __shutdown_and_exit(self, dummyServiceId, dummyPayload):
        logging.info("Shutting down the Yavide server ...")
        self.__shutdown_all_services(dummyServiceId, dummyPayload)
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
        logging.info("Yavide server shut down.")

def handle_exception(exc_type, exc_value, exc_traceback):
    logging.critical("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))

def catch_unhandled_exceptions():
    # This is what usually should be enough
    sys.excepthook = handle_exception

    # But sys.excepthook does not work anymore within multi-threaded/multi-process environment (see https://bugs.python.org/issue1230540)
    # So what we can do is to override the YavideService.listen() implementation so it includes try-catch block with exceptions
    # being forwarded to the sys.excepthook function.
    run_original = YavideService.listen
    def listen(self):
        try:
            run_original(self)
        except:
            sys.excepthook(*sys.exc_info())
    YavideService.listen = listen

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
        YavideServer(msg_queue, yavide_instance).listen()
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

