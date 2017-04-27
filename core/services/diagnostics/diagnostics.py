import logging
import time

class Diagnostics():
    def __init__(self, tunit_pool, parser, callback = None):
        self.tunit_pool = tunit_pool
        self.parser = parser
        self.callback = callback

    def __call__(self, args):
        diagnostics_iter = self.parser.get_diagnostics(self.tunit_pool[str(args[0])])
        if self.callback and diagnostics_iter:
            self.callback(diagnostics_iter, args)
