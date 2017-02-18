import logging
from yavide_service import YavideService
from services.indexer.yavide_indexer import YavideSourceCodeIndexer
from services.indexer.yavide_indexer import YavideSourceCodeIndexerParams

class SourceCodeIndexer(YavideService):
    def __init__(self, server_queue, yavide_instance):
        YavideService.__init__(self, server_queue, yavide_instance, self.__startup_hook, self.__shutdown_hook)
        self.src_code_indexer = ""

    def __startup_hook(self, args):
        logging.info("Args = {0}.".format(args))

        file_types_len = int(args[0])
        file_types = args[1:file_types_len]
        proj_root_directory = args[file_types_len + 1]
        proj_cxx_tags_filename = args[file_types_len + 2]
        proj_java_tags_filename = args[file_types_len + 3]
        proj_cscope_db_filename = args[file_types_len + 4]
        logging.info("file_types_len = {0}, file_types = {1}, proj_root_dir = {2}, proj_cxx_tags = {3}, proj_java_tags = {4}, proj_cscope_db = {5}".format(file_types_len, file_types, proj_root_directory, proj_cxx_tags_filename, proj_java_tags_filename, proj_cscope_db_filename))

        self.src_code_indexer = YavideSourceCodeIndexer(
            YavideSourceCodeIndexerParams(
                self.yavide_instance,
                file_types,
                proj_root_directory,
                proj_cxx_tags_filename,
                proj_java_tags_filename,
                proj_cscope_db_filename
            )
        )
        self.src_code_indexer.start()
        logging.info("Indexer started ...")

    def __shutdown_hook(self, payload):
        logging.info("Shutting down the indexer ...")
        self.src_code_indexer.stop()

