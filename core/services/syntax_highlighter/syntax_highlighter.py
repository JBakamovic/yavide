import logging
import time

class SyntaxHighlighter():
    def __init__(self, indexer, callback = None):
        self.indexer = indexer
        self.callback = callback

    def __call__(self, args):
        if self.callback:
            self.callback(self.indexer.get_tunit(str(args[0])), self.indexer.get_parser(), args)

