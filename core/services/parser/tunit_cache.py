import os
from collections import OrderedDict

class UnlimitedCache():
    def __init__(self):
        self.store = {}

    def iterkeys(self):
        return self.store.iterkeys()

    def itervalues(self):
        return self.store.itervalues()

    def iteritems(self):
        return self.store.iteritems()

    def __getitem__(self, key):
        return self.store[key]

    def __setitem__(self, key, value):
        if key in self.store:
            del self.store[key]
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

    def iterkeys(self):
        return self.store.iterkeys()

    def itervalues(self):
        return self.store.itervalues()

    def iteritems(self):
        return self.store.iteritems()

    def __getitem__(self, key):
        return self.store[key]

    def __setitem__(self, key, value):
        if key in self.store:
            del self.store[key]
        else:
            if len(self.store) == self.max_capacity:
                self.store.popitem(last=False) # last=False --> FIFO, last=True --> LIFO
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
        return (None, None,)

    def insert(self, tunit_filename, tunit):
        pass

    def iterkeys(self):
        return None

    def itervalues(self):
        return None

    def iteritems(self):
        return None

    def __setitem__(self, key, item):
        self.insert(key, item)

    def __getitem__(self, key):
        return self.fetch(key)

    def __iter__(self):
        return None

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

    def iterkeys(self):
        return self.tunit.iterkeys()

    def itervalues(self):
        return self.tunit.itervalues()

    def iteritems(self):
        return self.tunit.iteritems()

    def __setitem__(self, key, item):
        self.insert(key, item)

    def __getitem__(self, key):
        return self.fetch(key)

    def __iter__(self):
        return self.tunit.__iter__()

    def __len__(self):
        return len(self.tunit)

