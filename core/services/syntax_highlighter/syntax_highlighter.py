import logging
import time

class SyntaxHighlighter():
    def __init__(self, parser, callback = None):
        self.parser = parser
        self.callback = callback

    def __call__(self, args):
        if self.callback:
            self.callback(self.parser, args)

