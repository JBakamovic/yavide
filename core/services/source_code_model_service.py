import logging
from services.yavide_service import YavideService
from services.syntax_highlighter.syntax_highlighter import SyntaxHighlighter
from services.diagnostics.diagnostics import Diagnostics
from services.indexer.clang_indexer import ClangIndexer
from services.type_deduction.type_deduction import TypeDeduction
from services.go_to_definition.go_to_definition import GoToDefinition
from services.go_to_include.go_to_include import GoToInclude
from services.parser.clang_parser import ClangParser
from services.parser.tunit_cache import TranslationUnitCache, FifoCache

class SourceCodeModel(YavideService):
    def __init__(self, service_plugin):
        YavideService.__init__(self, service_plugin)
        self.parser = None
        self.service = {}

    def __unknown_service(self, args):
        logging.error("Unknown service triggered! Valid services are: {0}".format(self.service))

    def startup_callback(self, args):
        project_root_directory = args[0]
        compiler_args_filename = args[1]

        # Instantiate source-code-model services with Clang parser configured
        self.parser        = ClangParser(compiler_args_filename, TranslationUnitCache(FifoCache(20)))
        self.clang_indexer = ClangIndexer(self.parser, project_root_directory)
        self.service = {
            0x0 : self.clang_indexer,
            0x1 : SyntaxHighlighter(self.parser),
            0x2 : Diagnostics(self.parser),
            0x3 : TypeDeduction(self.parser),
            0x4 : GoToDefinition(self.parser, self.clang_indexer.get_symbol_db()),
            0x5 : GoToInclude(self.parser)
        }

    def shutdown_callback(self, args):
        pass

    def __call__(self, args):
        return self.service.get(int(args[0]), self.__unknown_service)(args[1:len(args)])
