""" Class to manage database connections. """
import sqlite3

from lib.movies_constants import DATABASE_FILE


class ConnectionManager:
    """ Connection Manager class to manage database connections """
    _connection = None

    def __init__(self):
        """ Creates a connection to the database """
        self._connect()

    def _connect(self):
        """ Connects to the database """
        self._connection = sqlite3.connect(DATABASE_FILE, timeout=10)

    def get_connection(self):
        """ Returns the connection """
        return self._connection

    def reconnect(self):
        """ Reconnects to the database """
        self._connect()
