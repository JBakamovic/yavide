import logging
from multiprocessing import Queue

class Service():
    def __init__(self, service_plugin):
        self.queue = Queue()
        self.service_plugin = service_plugin
        self.action = {
            0x0 : self.__startup_request,
            0x1 : self.__shutdown_request,
            0x2 : self.__request
        }
        self.keep_listening = True
        logging.info("Actions: {0}".format(self.action))

    def __startup_request(self, payload):
        logging.info("Service startup ... Payload = {0}".format(payload))
        self.startup_callback(payload)
        self.service_plugin.startup_callback(True, payload)

    def __shutdown_request(self, payload):
        logging.info("Service shutdown ... Payload = {0}".format(payload))
        self.shutdown_callback(payload)
        self.service_plugin.shutdown_callback(True, payload)
        self.keep_listening = False

    def __request(self, payload):
        success, args = self.__call__(payload)
        self.service_plugin.__call__(success, args, payload)

    def __unknown_action(self, payload):
        logging.error("Unknown action triggered! Valid actions are: {0}".format(self.action))

    def listen(self):
        while self.keep_listening is True:
            logging.info("Listening on a request ...")
            payload = self.queue.get()
            logging.info("Request received. Payload = {0}".format(payload))
            self.action.get(payload[0], self.__unknown_action)(payload[1])
        logging.info("Service shut down.")

    def send_startup_request(self, payload):
        self.queue.put([0x0, payload])

    def send_shutdown_request(self, payload):
        self.queue.put([0x1, payload])

    def send_request(self, payload):
        self.queue.put([0x2, payload])
