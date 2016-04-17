import sys
import argparse
import time
import shlex
import os.path
import logging
import threading
import SocketServer
import yavide_utils

from multiprocessing import Process, Queue, Pool

class ServiceBase:
   def worker_thread(self):
      return self.__worker_thread_impl()

   def __worker_thread_impl(self):
      print "Hello from ServiceBase worker thread implementation!"

class IndexerService(ServiceBase):
   def __worker_thread_impl(self):
      print "Hello from IndexerService worker thread implementation!"

class VimCmdHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        while True:
            data = self.request.recv(16)
            if data:
                print self.server.services
                print "VimCmdHandler thread[{0}]: Request from {1} ...".format(threading.current_thread().name, self.client_address)
                #time.sleep(3)
                print "VimCmdHandler received data {0} ...".format(data)
                #yavide_utils.YavideUtils.send_vim_remote_command("YAVIDE", ":" + data)
                self.server.services.worker_thread()

class VimCmdDispatcher(SocketServer.TCPServer):
    def __init__(self, address, port, services):
        self.host_addr = address
        self.port = port
        self.cmd_handler = VimCmdHandler
        self.services = services
        SocketServer.TCPServer.__init__(self, (self.host_addr, self.port), VimCmdHandler)

class VimCmdServer():
    def __init__(self, address, port):
        self.host_addr = address
        self.port = port
        self.services = IndexerService()
        self.server = VimCmdDispatcher(self.host_addr, self.port, self.services)

    def run(self):
        print "VimCmdDispatcher [{0}]: Listening on port {1}".format(threading.current_thread().name, self.port)
        self.server.serve_forever()

def main():
    parser = argparse.ArgumentParser()
    #parser.add_argument("port", help="server will listen on this port")
    args = parser.parse_args()

    FORMAT = '[%(levelname)s] [%(filename)s:%(lineno)s] %(funcName)25s(): %(message)s'
    logging.basicConfig(filename='.yavide_indexer.log', filemode='w', format=FORMAT, level=logging.INFO)

    cmd_server = VimCmdServer('localhost', int(args.port))
    cmd_server.run()

if __name__ == "__main__":
    main()

