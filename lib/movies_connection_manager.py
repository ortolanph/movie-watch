import sqlite3

from lib.movies_constants import DATABASE_FILE


class ConnectionManager:
    _connection = None

    def __init__(self):
        self._connection = sqlite3.connect(DATABASE_FILE, timeout=10)

    def get_connection(self):
        return self._connection
