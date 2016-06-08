import logging
from multiprocessing import Queue

class YavideService():
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

