import sqlite3

class SymbolDatabase(object):
    def __init__(self, db_filename = None):
        self.filename = db_filename
        if db_filename:
            self.db_connection = sqlite3.connect(db_filename)
        else:
            self.db_connection = None

    def __del__(self):
        if self.db_connection:
            self.db_connection.close()

    def open(self, db_filename):
        if not self.db_connection:
            self.db_connection = sqlite3.connect(db_filename)
            self.filename = db_filename

    def close(self):
        if self.db_connection:
            self.db_connection.close()
            self.db_connection = None

    def is_open(self):
        return self.db_connection != None

    def get_all(self):
        # TODO Use generators
        return self.db_connection.cursor().execute('SELECT * FROM symbol')

    def get_by_id(self, id):
        return self.db_connection.cursor().execute('SELECT * FROM symbol WHERE usr=?', (id,))

    def get_definition(self, id):
        return self.db_connection.cursor().execute('SELECT * FROM symbol WHERE usr=? AND is_definition=1', (id,))

    def insert_single(self, filename, line, column, unique_id, context, symbol_kind, is_definition):
        try:
            self.db_connection.cursor().execute('INSERT INTO symbol VALUES (?, ?, ?, ?, ?, ?, ?)',
                (filename, line, column, unique_id, context, symbol_kind, is_definition,)
            )
        except sqlite3.IntegrityError:
            pass

    def flush(self):
        self.db_connection.commit()

    def delete(self, filename):
        self.db_connection.cursor().execute('DELETE FROM symbol WHERE filename=?', (filename,))

    def delete_all(self):
        self.db_connection.cursor().execute('DELETE FROM symbol')

    def create_data_model(self):
        self.db_connection.cursor().execute(
            'CREATE TABLE IF NOT EXISTS symbol ( \
                filename        text,            \
                line            integer,         \
                column          integer,         \
                usr             text,            \
                context         text,            \
                kind            integer,         \
                is_definition   boolean,         \
                PRIMARY KEY(filename, usr, line) \
             )'
        )

