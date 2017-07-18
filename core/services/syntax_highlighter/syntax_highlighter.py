import logging
import time

class SyntaxHighlighter():
    def __init__(self, tunit_pool, parser, callback = None):
        self.tunit_pool = tunit_pool
        self.parser = parser
        self.callback = callback

    def __call__(self, args):
        if self.callback:
            self.callback(self.tunit_pool[str(args[0])], self.parser, args)
