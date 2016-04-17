import os
import argparse
import socket
import time
from multiprocessing.connection import Client

class TcpClient():
    def __init__(self, server_address, server_port):
        self.server_address = server_address
        self.server_port = server_port
    
    def connect(self):
        print "Connecting to the server: {0}:{1}".format(self.server_address, self.server_port)
        self.conn = Client((self.server_address, self.server_port))

    def send(self, data):
        print "Sending some data ..."
        self.conn.send(data)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("port", help="client will try to connect to this port")
    parser.add_argument("data", help="give some data to be transfered to the server")
    args = parser.parse_args()
    
    vim_cmd = "echo " + args.data
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('localhost', int(args.port)))
    while True:
         print "Sending {0}".format(vim_cmd)
         sock.sendall(vim_cmd)
         time.sleep(3)

    #client = TcpClient('localhost', int(args.port))
    #client.connect()
    #client.send(args.data)

if __name__ == "__main__":
    main()
