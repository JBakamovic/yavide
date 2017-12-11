import logging
from multiprocessing import Queue

class YavideService():
    def __init__(self, yavide_instance, startup_callback, shutdown_callback, request_callback):
        self.queue = Queue()
        self.yavide_instance = yavide_instance # TODO remove
        self.startup_callback = startup_callback
        self.shutdown_callback = shutdown_callback
        self.request_callback = request_callback
        self.action = {
            0x0 : self.__startup_request,
            0x1 : self.__shutdown_request,
            0x2 : self.__request
        }
        self.keep_listening = True
        logging.info("Yavide instance: {0}".format(self.yavide_instance))
        logging.info("Actions: {0}".format(self.action))

    def __startup_request(self, payload):
        # TODO define an API to expose startup request to client plugin
        logging.info("Service startup ... Payload = {0}".format(payload))
        self.startup_callback(payload)

    def __shutdown_request(self, payload):
        # TODO define an API to expose shutdown request to client plugin
        logging.info("Service shutdown ... Payload = {0}".format(payload))
        self.shutdown_callback(payload)
        self.keep_listening = False

    def __request(self, payload):
        success, args = self.__call__(payload)
        self.request_callback(success, args, payload)

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
