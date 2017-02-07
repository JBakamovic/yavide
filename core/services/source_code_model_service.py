import logging
from yavide_service import YavideService
from services.parser.clang_parser import ClangParser
from syntax_highlighter.syntax_highlighter import SyntaxHighlighter
from services.vim.syntax_generator import VimSyntaxGenerator

class SourceCodeModel(YavideService):
    def __init__(self, server_queue, yavide_instance):
        YavideService.__init__(self, server_queue, yavide_instance)
        self.parser = ClangParser()
        self.service = {
            0x0 : SyntaxHighlighter(self.parser, VimSyntaxGenerator(yavide_instance, "/tmp/yavideSyntaxFile.vim"))
        }

    def unknown_service(self):
        pass

    def run_impl(self, args):
        self.service.get(int(args[0]), self.unknown_service)(args[1:len(args)])

