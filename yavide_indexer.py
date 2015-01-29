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
            self.db_generate()

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
    def db_generate(self):
        print "[YavideCtagsIndexer]: Generating initial tags"
        self.db_generate_impl(0, self.root_directory)

    def db_delete_entry(self, filename):
        cmd = 'sed -i ' + '"' + '\:' + os.path.basename(filename) + ':d' + '" ' + os.path.join(self.root_directory, self.tags_filename)
        print "[YavideCtagsIndexer]: " + cmd
        call(shlex.split(cmd))

    def update(self, filename, event_type):
        print "[YavideCtagsIndexer]: Root directory: {0}".format(self.root_directory)
        YavideIndexerBase.update(self, filename, event_type)

class YavideCtagsIndexer_Cxx(YavideCtagsIndexer):
    def db_generate_impl(self, doDbUpdate, files):
        cmd  = 'ctags --languages=C,C++ --c++-kinds=+p --fields=+iaS --extra=+q '
        cmd += '-a ' if (doDbUpdate == 1) else '-R '
        cmd += '-f ' + os.path.join(self.root_directory, self.tags_filename) + ' "' + files + '"'
        print "[YavideCtagsIndexer_Cxx]: " + cmd
        call(shlex.split(cmd))

    def on_create(self, filename):
        print "[YavideCtagsIndexer_Cxx]: File created"

    def on_delete(self, filename):
        print "[YavideCtagsIndexer_Cxx]: File deleted"

    def on_modify(self, filename):
        print "[YavideCtagsIndexer_Cxx]: File modified"

        # Remove all entries from tags database which are referencing the given filename
        self.db_delete_entry(filename)

        # Rebuild the tags database for the given filename
        self.db_generate_impl(1, filename)

    def on_move(self, filename):
        print "[YavideCtagsIndexer_Cxx]: File moved"

class YavideCtagsIndexer_Java(YavideCtagsIndexer):
    def db_generate_impl(self, doDbUpdate, files):
        cmd  = 'ctags --languages=Java --extra=+q '
        cmd += '-a ' if (doDbUpdate == 1) else '-R '
        cmd += '-f ' + os.path.join(self.root_directory, self.tags_filename) + ' "' + files + '"'
        print "[YavideCtagsIndexer_Java]: " + cmd
        call(shlex.split(cmd))

    def on_create(self, filename):
        print "[YavideCtagsIndexer_Java]: File created"

    def on_delete(self, filename):
        print "[YavideCtagsIndexer_Java]: File deleted"

    def on_modify(self, filename):
        print "[YavideCtagsIndexer_Java]: File modified"

        # Remove all entries from tags database which are referencing the given filename
        self.db_delete_entry(filename)

        # Rebuild the tags database for the given filename
        self.db_generate_impl(1, filename)

    def on_move(self, filename):
        print "[YavideCtagsIndexer_Java]: File moved"

class YavideCScopeIndexer(YavideIndexerBase):
    def __init__(self, yavide_instance, root_directory, tags_filename, file_types):
        self.file_types = file_types
        self.yavide_instance = yavide_instance
        YavideIndexerBase.__init__(self, root_directory, tags_filename)
        self.db_set_default_params()
        self.db_add()

    def db_generate(self):
        print "[YavideCScopeIndexer]: Generating initial tags"
        self.db_generate_impl(0)
        self.db_add()

    def db_set_default_params(self):
        cmd = ':set cscopetag | set cscopetagorder=0'
        YavideUtils.send_vim_remote_command(self.yavide_instance, cmd)

    def db_add(self):
        cmd = ':cscope add ' + os.path.join(self.root_directory, self.tags_filename)
        YavideUtils.send_vim_remote_command(self.yavide_instance, cmd)

    def db_reset(self):
        YavideUtils.send_vim_remote_command(self.yavide_instance, ":cscope reset")

    def update(self, filename, event_type):
        print "[YavideCScopeIndexer]: Root directory: {0}".format(self.root_directory)
        YavideIndexerBase.update(self, filename, event_type)
        self.db_reset()

    def on_create(self, filename):
        print "[YavideCScopeIndexer]: File created"

    def on_delete(self, filename):
        print "[YavideCScopeIndexer]: File deleted"

    def on_modify(self, filename):
        print "[YavideCScopeIndexer]: File modified"
        self.db_generate_impl(1)

    def on_move(self, filename):
        print "[YavideCScopeIndexer]: File moved"

    def db_generate_file_list(self):
        cmd = 'find .'
        length = len(self.file_types)
        for i, ext in enumerate(self.file_types):
            cmd += ' -iname *' + ext
            if (i != length-1):
                cmd += ' -o'
        print "[YavideCScopeIndexer]: " + cmd
        f = open(os.path.join(self.root_directory, 'cscope.files'), "w")
        p = subprocess.Popen(shlex.split(cmd), stdout=f, shell=False, cwd=self.root_directory)
        p.wait()
        f.close()

    def db_generate_impl(self, doDbUpdate):
        self.db_generate_file_list()
        cmd  = 'cscope -q -R -b'
        cmd += ' -U' if (doDbUpdate == 1) else ''
        print "[YavideCScopeIndexer]: " + cmd
        p = subprocess.Popen(shlex.split(cmd), shell=False, cwd=self.root_directory)
        p.wait()
        print "[YavideCScopeIndexer]: Finished!"

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
        print "File extension whitelist: {0}".format(self.file_types_whitelist)
        print "Indexers:"
        for prog_language in programming_languages:
            print "\t[{0}]".format(prog_language)
            indexers = self.indexers[prog_language]
            for indexer in indexers:
                print "\t\t {0}".format(indexer)

    def run(self):
        self.observer.start()

    def stop(self):
        self.observer.stop()

    def finalize(self):
        self.observer.join()

    def update(self, filename, event_type):
        file_type = os.path.splitext(filename)[1]
        print "[YavideSourceCodeIndexer] Filename: {0} Extension: {1}".format(filename, file_type)
        if file_type in self.file_types_whitelist:
            programming_language = YavideUtils.file_type_to_programming_language(file_type)
            print "[YavideSourceCodeIndexer] ProgLanguage: {0}".format(programming_language)
            if programming_language in self.indexers:
                print "[YavideSourceCodeIndexer]: Filename: {0} Event_type: {1}".format(filename, event_type)
                indexers = self.indexers[programming_language]
                for indexer in indexers:
                    indexer.update(filename, event_type)

if __name__ == "__main__":
    # Parse the indexer parameters
    yavide_instance = sys.argv[1]
    offset = int(sys.argv[2])
    file_types = []
    for idx, param in enumerate(sys.argv):
        if idx > 2 and idx < 3 + offset:
            file_types.append(param)
    proj_root_directory = sys.argv[3 + offset]
    proj_cxx_tags_filename = sys.argv[4 + offset]
    proj_java_tags_filename = sys.argv[5 + offset]
    proj_cscope_db_filename = sys.argv[6 + offset]

    # Run the indexer
    indexer = YavideSourceCodeIndexer(
                YavideSourceCodeIndexerParams(
                    yavide_instance, file_types,
                    proj_root_directory, proj_cxx_tags_filename,
                    proj_java_tags_filename, proj_cscope_db_filename)
    )
    indexer.run()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        indexer.stop()
    indexer.finalize()

