import sys
import time
import shlex
import os.path
import logging
import subprocess
from subprocess import call
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from multiprocessing.connection import Listener
from common.yavide_utils import YavideUtils

class YavideIndexerBase():
    def __init__(self, root_directory, tags_filename):
        self.root_directory = root_directory
        self.tags_filename = tags_filename
        self.action = {
                'created'   : self.on_create,
                'deleted'   : self.on_delete,
                'modified'  : self.on_modify,
                'moved'     : self.on_move
        }

        # If no tags db is available, generate one
        if os.path.isfile(os.path.join(self.root_directory, self.tags_filename)) == False:
            logging.info('Generating initial tags db.')
            self.db_generate()

    def update(self, filename, event_type):
        logging.info("Triggering update process on '{0}' event.".format(event_type))
        self.action[event_type](filename)

    def on_create(self, filename):
        return

    def on_delete(self, filename):
        return

    def on_modify(self, filename):
        return

    def on_move(self, filename):
        return

class YavideCtagsIndexer(YavideIndexerBase):
    def db_generate(self):
        self.db_generate_impl(0, self.root_directory)

    def db_delete_entry(self, filename):
        cmd = 'sed -i ' + '"' + '\:' + os.path.basename(filename) + ':d' + '" ' + os.path.join(self.root_directory, self.tags_filename)
        logging.info("Deleting an entry from db: '{0}'".format(cmd))
        call(shlex.split(cmd))

    def update(self, filename, event_type):
        YavideIndexerBase.update(self, filename, event_type)

class YavideCtagsIndexer_Cxx(YavideCtagsIndexer):
    def db_generate_impl(self, doDbUpdate, files):
        cmd  = 'ctags --languages=C,C++ --c++-kinds=+p --fields=+iaS --extra=+q '
        cmd += '-a ' if (doDbUpdate == 1) else '-R '
        cmd += '-f ' + os.path.join(self.root_directory, self.tags_filename) + ' "' + files + '"'
        logging.info("Generating the db: '{0}'".format(cmd))
        call(shlex.split(cmd))

    def on_create(self, filename):
        logging.info("File created: '{0}'".format(os.path.basename(filename)))

        # Rebuild the tags database for the given filename
        self.db_generate_impl(1, filename)

    def on_delete(self, filename):
        logging.info("File deleted: '{0}'".format(os.path.basename(filename)))

        # Remove all entries from tags database which are referencing the given filename
        self.db_delete_entry(filename)

    def on_modify(self, filename):
        logging.info("File modified: '{0}'".format(os.path.basename(filename)))

        # Remove all entries from tags database which are referencing the given filename
        self.db_delete_entry(filename)

        # Rebuild the tags database for the given filename
        self.db_generate_impl(1, filename)

    def on_move(self, filename):
        logging.info("File moved: '{0}'".format(os.path.basename(filename)))

        # Remove all entries from tags database which are referencing the given filename
        self.db_delete_entry(filename)

        # Rebuild the tags database for the given filename
        self.db_generate_impl(1, filename)

class YavideCtagsIndexer_Java(YavideCtagsIndexer):
    def db_generate_impl(self, doDbUpdate, files):
        cmd  = 'ctags --languages=Java --extra=+q '
        cmd += '-a ' if (doDbUpdate == 1) else '-R '
        cmd += '-f ' + os.path.join(self.root_directory, self.tags_filename) + ' "' + files + '"'
        logging.info("Generating the db: '{0}'".format(cmd))
        call(shlex.split(cmd))

    def on_create(self, filename):
        logging.info("File created: '{0}'".format(os.path.basename(filename)))

        # Rebuild the tags database for the given filename
        self.db_generate_impl(1, filename)

    def on_delete(self, filename):
        logging.info("File deleted: '{0}'".format(os.path.basename(filename)))

        # Remove all entries from tags database which are referencing the given filename
        self.db_delete_entry(filename)

    def on_modify(self, filename):
        logging.info("File modified: '{0}'".format(os.path.basename(filename)))

        # Remove all entries from tags database which are referencing the given filename
        self.db_delete_entry(filename)

        # Rebuild the tags database for the given filename
        self.db_generate_impl(1, filename)

    def on_move(self, filename):
        logging.info("File moved: '{0}'".format(os.path.basename(filename)))

        # Remove all entries from tags database which are referencing the given filename
        self.db_delete_entry(filename)

        # Rebuild the tags database for the given filename
        self.db_generate_impl(1, filename)

class YavideCScopeIndexer(YavideIndexerBase):
    def __init__(self, yavide_instance, root_directory, tags_filename, file_types):
        self.file_types = file_types
        self.yavide_instance = yavide_instance
        self.source_file_list_db = 'cscope.files'
        YavideIndexerBase.__init__(self, root_directory, tags_filename)
        self.db_set_default_params()
        self.db_add()

    def db_generate(self):
        self.db_generate_impl(0)
        self.db_add()

    def db_set_default_params(self):
        cmd = ':set cscopetag | set cscopetagorder=0'
        YavideUtils.send_vim_remote_command(self.yavide_instance, cmd)
        logging.info("Setting default parameters: '{0}'".format(cmd))

    def db_add(self):
        cmd = ':cscope add ' + os.path.join(self.root_directory, self.tags_filename)
        YavideUtils.send_vim_remote_command(self.yavide_instance, cmd)
        logging.info("Adding a new db connection: '{0}'".format(cmd))

    def db_reset(self):
        cmd = ':cscope reset'
        YavideUtils.send_vim_remote_command(self.yavide_instance, cmd)
        logging.info("Resetting the db connection: '{0}'".format(cmd))

    def update(self, filename, event_type):
        YavideIndexerBase.update(self, filename, event_type)
        self.db_reset()

    def on_create(self, filename):
        logging.info("File created: '{0}'".format(os.path.basename(filename)))

        # Insert a corresponding file entry
        self.db_add_file_entry(filename)

        # Rebuild the tags database for the given filename
        self.db_generate_impl(1)

    def on_delete(self, filename):
        logging.info("File deleted: '{0}'".format(os.path.basename(filename)))

        # Remove a corresponding file entry
        self.db_delete_file_entry(filename)

        # Rebuild the tags database for the given filename
        self.db_generate_impl(1)

    def on_modify(self, filename):
        logging.info("File modified: '{0}'".format(os.path.basename(filename)))

        # Rebuild the tags database for the given filename
        self.db_generate_impl(1)

    def on_move(self, filename):
        logging.info("File moved: '{0}'".format(os.path.basename(filename)))

        # Replace a corresponding file entry
        self.db_replace_file_entry(filename)

        # Rebuild the tags database for the given filename
        self.db_generate_impl(1)

    def db_add_file_entry(self, filename):
        if not self.__file_db_exists():
            self.db_generate_file_list()
        else:
            cmd = 'sed -i ' + '"' + '\$a' + './' + os.path.relpath(filename, self.root_directory) + '" ' + os.path.join(self.root_directory, self.source_file_list_db)
            logging.info("Adding an entry to source file list db: '{0}'".format(cmd))
            call(shlex.split(cmd))

    def db_delete_file_entry(self, filename):
        if not self.__file_db_exists():
            self.db_generate_file_list()
        else:
            cmd = 'sed -i ' + '"' + '\:' + os.path.relpath(filename, self.root_directory) + ':d' + '" ' + os.path.join(self.root_directory, self.source_file_list_db)
            logging.info("Deleting an entry from source file list db: '{0}'".format(cmd))
            call(shlex.split(cmd))

    def db_replace_file_entry(self, filename):
        if not self.__file_db_exists():
            self.db_generate_file_list()
        else:
            # TODO  This can be optimized by using sed replace expression but we are missing an information about the destination filename.
            #       Destination filename information is provided by the handled event objects but it was not anticipated that this kind 
            #       of information will be required.
            self.db_generate_file_list()
            #cmd = 'sed -i ' + '"' + '\:' + os.path.relpath(src_filename, self.root_directory) + ':c' + dest_filename + " ' + os.path.join(self.root_directory, self.source_file_list_db)
            #logging.info("Replacing an entry in source file list db: '{0}'".format(cmd))
            #call(shlex.split(cmd))

    def db_generate_file_list(self):
        cmd = 'find .'
        length = len(self.file_types)
        for i, ext in enumerate(self.file_types):
            cmd += ' -iname *' + ext
            if (i != length-1):
                cmd += ' -o'
        logging.info("Generating file list: '{0}'".format(cmd))
        f = open(os.path.join(self.root_directory, self.source_file_list_db), "w")
        p = subprocess.Popen(shlex.split(cmd), stdout=f, shell=False, cwd=self.root_directory)
        p.wait()
        f.close()

    def db_generate_impl(self, doDbUpdate):
        if not self.__file_db_exists():
            self.db_generate_file_list()
        cmd  = 'cscope -q -R -b'
        cmd += ' -U' if (doDbUpdate == 1) else ''
        logging.info("Generating the db: '{0}'".format(cmd))
        p = subprocess.Popen(shlex.split(cmd), shell=False, cwd=self.root_directory)
        p.wait()

    def __file_db_exists(self):
        return os.path.isfile(os.path.join(self.root_directory, self.source_file_list_db))

class YavideFileSystemEventHandler(FileSystemEventHandler):
    def __init__(self, indexer):
        self.last_event = 'None'
        self.indexer = indexer

    def on_any_event(self, event):
        if event.is_directory == False:             # TODO do we need to track directory changes as well?
            if event.event_type == 'modified':
                if self.last_event != 'created':    # After new file gets created, two events get fired. Ignore the second one.
                    self.indexer.update(event.src_path, event.event_type)
            else:
                self.indexer.update(event.src_path, event.event_type)
            self.last_event = event.event_type

class YavideSourceCodeIndexerFactory():
    @staticmethod
    def getIndexer(programming_language, params):
        if (programming_language == 'Cxx'):
            return [ YavideCtagsIndexer_Cxx(params.proj_root_directory, params.proj_cxx_tags_filename),
                     YavideCScopeIndexer(params.yavide_instance, params.proj_root_directory,
                         params.proj_cscope_db_filename, params.file_types)
                   ]
        elif (programming_language == 'Java'):
            return [ YavideCtagsIndexer_Java(params.proj_root_directory, params.proj_java_tags_filename),
                     YavideCScopeIndexer(params.yavide_instance, params.proj_root_directory,
                         params.proj_cscope_db_filename, params.file_types)
                   ]
        else:
            return

class YavideSourceCodeIndexerParams():
    def __init__(self, yavide_instance, file_types, proj_root_directory,
                 proj_cxx_tags_filename, proj_java_tags_filename, proj_cscope_db_filename):
        self.yavide_instance            = yavide_instance
        self.file_types                 = file_types
        self.proj_root_directory        = proj_root_directory
        self.proj_cxx_tags_filename     = proj_cxx_tags_filename
        self.proj_java_tags_filename    = proj_java_tags_filename
        self.proj_cscope_db_filename    = proj_cscope_db_filename

class YavideSourceCodeIndexer():
    def __init__(self, params):
        self.file_types_whitelist = params.file_types
        self.indexers             = {}

        # Build a list of indexers which correspond to the given file types
        programming_languages = set()
        for file_type in self.file_types_whitelist:
            programming_languages.add(YavideUtils.file_type_to_programming_language(file_type))
        for programming_language in programming_languages:
            self.indexers[programming_language] = YavideSourceCodeIndexerFactory.getIndexer(programming_language, params)

        # Setup the filesystem event monitoring
        self.event_handler = YavideFileSystemEventHandler(self)
        self.observer = Observer()
        self.observer.deamon = True
        self.observer.schedule(self.event_handler, params.proj_root_directory, recursive=True)

        # Print some debug information
        logging.info("File extension whitelist: {0}".format(self.file_types_whitelist))
        logging.info("Active indexers:")
        for prog_language in programming_languages:
            logging.info("For [{0}] programming language:".format(prog_language))
            indexers = self.indexers[prog_language]
            if indexers:
                for indexer in indexers:
                    logging.info("\t\t {0}".format(indexer))

    def run(self):
        self.observer.start()

    def stop(self):
        self.observer.stop()

    def finalize(self):
        self.observer.join()

    def update(self, filename, event_type):
        file_type = os.path.splitext(filename)[1]
        if file_type in self.file_types_whitelist:
            programming_language = YavideUtils.file_type_to_programming_language(file_type)
            if programming_language in self.indexers:
                logging.info("Filename: '{0}' Event_type: '{1}' Programming lang: '{2}'".format(
                    os.path.basename(filename), event_type, programming_language)
                )
                indexers = self.indexers[programming_language]
                for indexer in indexers:
                    indexer.update(filename, event_type)


class YavideCommandHandler():
    def __init__(self, port):
        self.host = 'localhost'
        self.port = port
        self.indexer_running = False
        self.indexer = None

    def run(self):
        while True:
            # Start the server
            server_shutdown = False
            logging.info("Listening on {0} port".format(self.port))
            listener = Listener((self.host, self.port))
            conn = listener.accept()
            logging.info("Connection accepted from {0}".format(listener.last_accepted))

            # Handle client requests
            while True:
                try:
                    msg = conn.recv()
                    if not msg: continue
                    logging.info('Client request: {0}'.format(msg))
                    if msg[0] == 'start' and self.indexer_running == False:
                        self.__start_indexer(msg)
                    elif msg[0] == 'stop' and self.indexer_running == True:
                        self.__stop_indexer()
                    elif msg[0] == 'shutdown':
                        server_shutdown = True
                        break
                    else:
                        logging.warning('Unknown client request.')
                except (EOFError):
                    logging.info('Connection closed.')
                    conn.close()
                    listener.close()
                    break

            # Handle shutdown request
            if server_shutdown == True:
                logging.info('Shutting the indexer down ...')
                break

        # Clean-up and exit
        conn.close()
        listener.close()
        if self.indexer != None:
            if self.indexer_running == True:
                self.__stop_indexer()
            self.indexer.finalize()
        logging.info('Exiting ...')

    def __start_indexer(self, msg):
        logging.info('Starting the indexer ...')
        yavide_instance = msg[1]
        offset = int(msg[2])
        file_types = []
        for idx, param in enumerate(msg):
            if idx > 2 and idx < 3 + offset:
                file_types.append(param)
        proj_root_directory = msg[3 + offset]
        proj_cxx_tags_filename = msg[4 + offset]
        proj_java_tags_filename = msg[5 + offset]
        proj_cscope_db_filename = msg[6 + offset]

        self.indexer = YavideSourceCodeIndexer(
                        YavideSourceCodeIndexerParams(
                            yavide_instance, file_types,
                            proj_root_directory, proj_cxx_tags_filename,
                            proj_java_tags_filename, proj_cscope_db_filename)
        )
        self.indexer.run()
        self.indexer_running = True

    def __stop_indexer(self):
        logging.info('Stopping the indexer ...')
        self.indexer.stop()
        self.indexer_running = False

def main():
    FORMAT = '[%(levelname)s] [%(filename)s:%(lineno)s] %(funcName)25s(): %(message)s'
    logging.basicConfig(filename='.yavide_indexer.log', filemode='w', format=FORMAT, level=logging.INFO)
    if len(sys.argv) > 1:
        logging.info('Starting a Yavide indexer server ...')
        cmd_handler = YavideCommandHandler(int(sys.argv[1]))
        cmd_handler.run()
    else:
        logging.error('Insufficient number of arguments.')

if __name__ == "__main__":
    main()

