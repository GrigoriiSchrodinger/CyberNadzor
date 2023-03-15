import logging
import sqlite3

logger = logging.getLogger('root')


class DataBaseManager(object):
    def __init__(self, path):
        self.connect = sqlite3.connect(path)
        self.cursor = self.connect.cursor()

    def create_tables(self):
        """
        CREATE TABLE users
        """
        self.request(
            "CREATE TABLE IF NOT EXISTS users ("
            "id INTEGER PRIMARY KEY, "
            "name_users TEXT NOT NULL, "
            "id_users TEXT NOT NULL)"
        )

    def request(self, query):
        self.cursor.execute(query)
        logger.info(f"execute - {query}")
        self.connect.commit()

    def __del__(self):
        logger.info(f"Connect close")
        self.connect.close()
