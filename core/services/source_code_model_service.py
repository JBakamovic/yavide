import logging
from yavide_service import YavideService
from syntax_highlighter.syntax_highlighter import SyntaxHighlighter
from services.vim.syntax_generator import VimSyntaxGenerator
from diagnostics.diagnostics import Diagnostics
from services.vim.quickfix_diagnostics import VimQuickFixDiagnostics
from indexer.clang_indexer import ClangIndexer
from services.vim.indexer import VimIndexer
from type_deduction.type_deduction import TypeDeduction
from services.vim.type_deduction import VimTypeDeduction

class SourceCodeModel(YavideService):
    def __init__(self, server_queue, yavide_instance):
        YavideService.__init__(self, server_queue, yavide_instance)
        self.indexer = ClangIndexer(VimIndexer(yavide_instance))
        self.service = {
            0x0 : self.indexer,
            0x1 : SyntaxHighlighter(self.indexer.tunits, self.indexer.parser, VimSyntaxGenerator(yavide_instance, "/tmp/yavideSyntaxFile.vim")),
            0x2 : Diagnostics(self.indexer.tunits, self.indexer.parser, VimQuickFixDiagnostics(yavide_instance)),
            0x3 : TypeDeduction(self.indexer.tunits, self.indexer.parser, VimTypeDeduction(yavide_instance))
        }

    def __unknown_service(self, args):
        logging.error("Unknown service triggered! Valid services are: {0}".format(self.service))

    def __call__(self, args):
        self.service.get(int(args[0]), self.__unknown_service)(args[1:len(args)])
