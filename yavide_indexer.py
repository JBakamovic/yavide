import sys
import time
import shlex
import os.path
import subprocess
from subprocess import call
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from yavide_utils import YavideUtils

class YavideIndexerBase():
    def __init__(self, root_directory):
        self.root_directory = root_directory
        self.action = {
                'created'   : self.on_create,
                'deleted'   : self.on_delete,
                'modified'  : self.on_modify,
                'moved'     : self.on_move
        }

    def update(self, filename, event_type):
        self.action[event_type](filename)

    def on_create(self, filename):
        print "[YavideIndexerBase]: File created"

    def on_delete(self, filename):
        print "[YavideIndexerBase]: File deleted"

    def on_modify(self, filename):
        print "[YavideIndexerBase]: File modified"

    def on_move(self, filename):
        print "[YavideIndexerBase]: File moved"

class YavideCtagsIndexer(YavideIndexerBase):
    def update(self, filename, event_type):
        print "[YavideCtagsIndexer]: Root directory: {0}".format(self.root_directory)
        YavideIndexerBase.update(self, filename, event_type)

class YavideCtagsIndexer_Cxx(YavideCtagsIndexer):
    def on_create(self, filename):
        print "[YavideCtagsIndexer_Cxx]: File created"

    def on_delete(self, filename):
        print "[YavideCtagsIndexer_Cxx]: File deleted"

    def on_modify(self, filename):
        print "[YavideCtagsIndexer_Cxx]: File modified"

        # Remove all the lines from tags database which are referencing the given filename
        cmd = 'sed -i ' + '"' + '\:' + os.path.basename(filename) + ':d' + '" ' + self.root_directory + '/.cxx_tags'
        print "[YavideCtagsIndexer_Cxx]: " + cmd
        call(shlex.split(cmd))

        # Rebuild the tags database for the given filename
        cmd = 'ctags --c++-kinds=+p --fields=+iaS --extra=+q -a -f ' + self.root_directory + '/.cxx_tags' + ' "' + filename + '"'
        print "[YavideCtagsIndexer_Cxx]: " + cmd
        call(shlex.split(cmd))

    def on_move(self, filename):
        print "[YavideCtagsIdexer_Cxx]: File moved"

class YavideCtagsIndexer_Java(YavideCtagsIndexer):
    def on_create(self, filename):
        print "[YavideCtagsIndexer_Java]: File created"

    def on_delete(self, filename):
        print "[YavideCtagsIndexer_Java]: File deleted"

    def on_modify(self, filename):
        print "[YavideCtagsIndexer_Java]: File modified"

        # Remove all the lines from tags database which are referencing the given filename
        cmd = 'sed -i ' + '"' + '\:' + os.path.basename(filename) + ':d' + '" ' + self.root_directory + '/.java_tags'
        print "[YavideCtagsIndexer_Java]: " + cmd
        call(shlex.split(cmd))

        # Rebuild the tags database for the given filename
        cmd = 'ctags --languages=Java --extra=+q -a -f ' + self.root_directory + '/.java_tags' + ' "' + filename + '"'
        print "[YavideCtagsIndexer_Java]: " + cmd
        call(shlex.split(cmd))

    def on_move(self, filename):
        print "[YavideCtagsIndexer_Java]: File moved"

class YavideCScopeIndexer(YavideIndexerBase):
    def __init__(self, yavide_instance, root_directory, programming_language):
        YavideIndexerBase.__init__(self, root_directory)
        self.programming_language_extension = YavideUtils.programming_language_to_extension(programming_language)
        self.cscope_files_path = os.path.join(self.root_directory, 'cscope.files')
        self.cscope_updated_cmd = ':silent cscope reset'
        self.yavide_instance = yavide_instance

    def update(self, filename, event_type):
        print "[YavideCScopeIndexer]: Root directory: {0}".format(self.root_directory)
        YavideIndexerBase.update(self, filename, event_type)
        cmd = 'vim --servername ' + self.yavide_instance + ' --remote-send "<ESC>' + self.cscope_updated_cmd + '<CR>"'
        call(shlex.split(cmd))

    def on_create(self, filename):
        print "[YavideCScopeIndexer]: File created"

    def on_delete(self, filename):
        print "[YavideCScopeIndexer]: File deleted"

    def on_modify(self, filename):
        print "[YavideCScopeIndexer]: File modified"

        # Pick up the files to build the database for
        cmd = 'find .'
        length = len(self.programming_language_extension)
        for i, ext in enumerate(self.programming_language_extension):
            cmd += ' -iname *' + ext
            if (i != length-1):
                cmd += ' -o'
        print "[YavideCScopeIndexer]: " + cmd
        f = open(self.cscope_files_path, "w")
        p = subprocess.Popen(shlex.split(cmd), stdout=f, shell=False, cwd=self.root_directory)
        p.wait()
        f.close()

        # Build the database
        cmd = 'cscope -q -R -U -b'
        print "[YavideCScopeIndexer]: " + cmd
        p = subprocess.Popen(shlex.split(cmd), shell=False, cwd=self.root_directory)
        p.wait()
        print "[YavideCScopeIndexer]: Finished!"

    def on_move(self, filename):
        print "[YavideCScopeIndexer]: File moved"

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

class YavideSourceCodeIndexer():
    def __init__(self, yavide_instance, root_directory):
        self.supported_indexers = {
            'Cxx'   : [YavideCtagsIndexer_Cxx(root_directory), YavideCScopeIndexer(yavide_instance, root_directory, 'Cxx')],
            'Java'  : [YavideCtagsIndexer_Java(root_directory), YavideCScopeIndexer(yavide_instance, root_directory, 'Java')],
        }
        self.event_handler = YavideFileSystemEventHandler(self)
        self.observer = Observer()
        self.observer.deamon = True
        self.observer.schedule(self.event_handler, root_directory, recursive=True)

    def run(self):
        self.observer.start()

    def stop(self):
        self.observer.stop()

    def wait(self):
        self.observer.join()

    def update(self, filename, event_type):
        file_extension = os.path.splitext(filename)[1]
        programming_lang = YavideUtils.file_extension_to_programming_language(file_extension)
        if programming_lang in self.supported_indexers:
            print "[YavideSourceCodeIndexer]: Filename: {0} Event_type: {1}".format(filename, event_type)
            indexers = self.supported_indexers[programming_lang]
            for indexer in indexers:
                indexer.update(filename, event_type)

if __name__ == "__main__":
    # TODO read '.yavide_proj' configuration file to setup the tag generation parameters
    # TODO pick-up the parameters like:
    #           root_directory,
    #           tags filenames,
    #           Yavide --servername instance,
    #           ctags & cscope user-configurable settings, etc.
    root_directory = sys.argv[1] if len(sys.argv) > 1 else '.'
    indexer = YavideSourceCodeIndexer('yavide', root_directory)
    indexer.run()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        indexer.stop()
    indexer.wait()

