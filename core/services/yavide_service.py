import logging
from multiprocessing import Queue

class YavideService():
    def __init__(self, server_queue, yavide_instance, startup_hook = None, shutdown_hook = None):
        self.queue = Queue()
        self.server_queue = server_queue
        self.yavide_instance = yavide_instance
        self.startup_hook = startup_hook
        self.shutdown_hook = shutdown_hook
        self.action = {
            0x0 : self.__startup_request,
            0x1 : self.__shutdown_request,
            0x2 : self.__request
        }
        self.keep_listening = True
        logging.info("Yavide instance: {0}".format(self.yavide_instance))
        logging.info("Actions: {0}".format(self.action))

    def __startup_request(self, payload):
        logging.info("Service startup ... Payload = {0}".format(payload))
        if self.startup_hook:
            self.startup_hook(payload)

    def __shutdown_request(self, payload):
        logging.info("Service shutdown ... Payload = {0}".format(payload))
        if self.shutdown_hook:
            self.shutdown_hook(payload)
        self.keep_listening = False

    def __request(self, payload):
        self.__call__(payload)

    def __unknown_action(self, payload):
        logging.error("Unknown action triggered! Valid actions are: {0}".format(self.action))

    def listen(self):
        while self.keep_listening is True:
            logging.info("Listening on a request ...")
            payload = self.queue.get()
            logging.info("Request received. Payload = {0}".format(payload))
            self.action.get(payload[0], self.__unknown_action)(payload[1])
        logging.info("Yavide service shut down.")

    def send_startup_request(self, payload):
        self.queue.put([0x0, payload])

    def send_shutdown_request(self, payload):
        self.queue.put([0x1, payload])

    def send_request(self, payload):
        self.queue.put([0x2, payload])
