import os

class NoneTranslationUnitCache():
    def __init__(self):
        pass

    def fetch(self, tunit_filename):
        return None

    def insert(self, tunit_filename, tunit):
        pass

    def drop(self, tunit_filename):
        pass

    def clear(self):
        pass

    def __len__(self):
        return 0

    def __setitem__(self, key, item):
        self.insert(key, item)

    def __getitem__(self, key):
        return self.fetch(key)

    def __delitem__(self, key):
        self.drop(key)

class TranslationUnitCache():
    def __init__(self):
        self.tunit = {}

    def fetch(self, tunit_filename):
        return self.tunit.get(tunit_filename, (None, None,))

    def insert(self, tunit_filename, tunit):
        self.drop(tunit_filename)
        self.tunit[tunit_filename] = (tunit, os.path.getmtime(tunit.spelling),)

    def drop(self, tunit_filename):
        if tunit_filename in self.tunit:
            del self.tunit[tunit_filename]

    def clear(self):
        self.tunit.clear()

    def __len__(self):
        return len(self.tunit)

    def __setitem__(self, key, item):
        self.insert(key, item)

    def __getitem__(self, key):
        return self.fetch(key)

    def __delitem__(self, key):
        self.drop(key)

