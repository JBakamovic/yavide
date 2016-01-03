import socket
import subprocess
from subprocess import call
import shlex

file_type_dict = {
    'Cxx': ['.c', '.cpp', '.cc', '.h', '.hpp'],
    'Java': ['.java'] }

class YavideUtils():
    @staticmethod
    def file_type_to_programming_language(file_type):
        for lang, file_types in file_type_dict.iteritems():
            if file_type in file_types:
                return lang

    @staticmethod
    def programming_language_to_extension(programming_language):
        return file_type_dict.get(programming_language, '')

    @staticmethod
    def send_vim_remote_command(vim_instance, command):
        cmd = 'gvim --servername ' + vim_instance + ' --remote-send "<ESC>' + command + '<CR>"'
        call(shlex.split(cmd))

    @staticmethod
    def call_vim_remote_function(vim_instance, function):
        cmd = 'gvim --servername ' + vim_instance + ' --remote-expr "' + function + '"'
        call(shlex.split(cmd))

    @staticmethod
    def is_port_available(port):
        s = socket.socket()
        try:
            s.bind(('localhost', port))
            s.close()
            return True
        except socket.error, msg:
            s.close()
            return False

    @staticmethod
    def get_available_port(port_begin, port_end):
        for port in range(port_begin, port_end):
            if YavideUtils.is_port_available(port) == True:
                return port
        return -1
