import logging
import time

class Diagnostics():
    def __init__(self, parser, callback = None):
        self.parser = parser
        self.callback = callback

    def __call__(self, args):
        diagnostics_iter = self.parser.get_diagnostics()
        if self.callback:
            self.callback(diagnostics_iter, args)
