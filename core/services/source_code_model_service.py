import logging
from yavide_service import YavideService
from services.syntax_highlighter.clang_tokenizer import ClangTokenizer
from syntax_highlighter.syntax_highlighter import SyntaxHighlighter

class SourceCodeModel(YavideService):
    def __init__(self, server_queue, yavide_instance):
        YavideService.__init__(self, server_queue, yavide_instance)
        self.tokenizer = ClangTokenizer()
        self.service = {
            0x0 : SyntaxHighlighter(self.tokenizer, yavide_instance)
        }

    def unknown_service(self):
        pass

    def run_impl(self, args):
        self.service.get(int(args[0]), self.unknown_service).run_impl(args[1:len(args)])

