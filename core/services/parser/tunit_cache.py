import os
from collections import OrderedDict

class UnlimitedCache():
    def __init__(self):
        self.store = {}

    def __getitem__(self, key):
        return self.store[key]

    def __setitem__(self, key, value):
        if key in self.store:
            del self.tunit[tunit_filename]
        self.store[key] = value

    def __delitem__(self, key):
        del self.store[key]

    def __iter__(self):
        return self.store.__iter__()

    def __len__(self):
        return len(self.store)

class FifoCache():
    def __init__(self, max_capacity):
        self.max_capacity = max_capacity
        self.store = OrderedDict()

    def __getitem__(self, key):
        return self.store[key]

    def __setitem__(self, key, value):
        if key not in self.store:
            if len(self.store) == self.max_capacity:
                self.store.popitem(last=False)
            self.store[key] = value

    def __delitem__(self, key):
        del self.store[key]

    def __iter__(self):
        return self.store.__iter__()

    def __len__(self):
        return len(self.store)

class NoneTranslationUnitCache():
    def __init__(self):
        pass

    def fetch(self, tunit_filename):
        return None

    def insert(self, tunit_filename, tunit):
        pass

    def __setitem__(self, key, item):
        self.insert(key, item)

    def __getitem__(self, key):
        return self.fetch(key)

    def __len__(self):
        return 0

class TranslationUnitCache():
    def __init__(self, cache=FifoCache(5)):
        self.tunit = cache

    def fetch(self, tunit_filename):
        if tunit_filename in self.tunit:
            return self.tunit[tunit_filename]
        return (None, None,)

    def insert(self, tunit_filename, tunit):
        self.tunit[tunit_filename] = (tunit, os.path.getmtime(tunit.spelling),)

    def __setitem__(self, key, item):
        self.insert(key, item)

    def __getitem__(self, key):
        return self.fetch(key)

    def __len__(self):
        return len(self.tunit)

