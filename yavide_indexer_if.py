import vim
import subprocess
import shlex
from multiprocessing.connection import Client
from yavide_utils import YavideUtils

def do_init():
    # Find first available port number
    port = YavideUtils.get_available_port(
                int(vim.eval('g:YAVIDE_SOURCE_CODE_INDEXER_PORT')),
                65535
    )

    # Save it in environment variable for later usage
    var = 'let g:YAVIDE_SOURCE_CODE_INDEXER_PORT = ' + str(port)
    vim.command(var)

    # Build a command string
    cmd = 'python '
    cmd += vim.eval('g:YAVIDE_SOURCE_CODE_INDEXER')
    cmd += ' '
    cmd += str(port)

    # Run the indexer server listening on a given port
    subprocess.Popen(shlex.split(cmd), shell=False)

def do_start():
    # Issue a command to start the indexing service with given params
    cmd = ['start']
    params = vim.eval('l:indexer_params')
    cmd += params.split()
    do_send(cmd)

def do_stop():
    # Issue a command to stop the indexing service
    cmd = ['stop']
    do_send(cmd)

def do_deinit():
    # Issue a command to shutdown the indexer server completely
    cmd = ['shutdown']
    do_send(cmd)

def do_send(cmd):
    # Send a command over 'localhost' TCP/IP
    conn = Client(('localhost', int(vim.eval('g:YAVIDE_SOURCE_CODE_INDEXER_PORT'))))
    conn.send(cmd)
    conn.close()

# Handle requests
if len(sys.argv) > 0:
    cmd = sys.argv[0]
    if cmd == 'init':
        do_init()
    elif cmd == 'start':
        do_start()
    elif cmd == 'stop':
        do_stop()
    elif cmd == 'deinit':
        do_deinit()

