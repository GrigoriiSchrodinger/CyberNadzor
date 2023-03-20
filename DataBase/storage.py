import logging
import sqlite3

logger = logging.getLogger('root')


class DataBaseManager(object):
    def __init__(self, path):
        self.connect = sqlite3.connect(path)
        self.cursor = self.connect.cursor()

    def create_tables(self):
        """
        CREATE TABLE:
        - users
        - below_track
        - higher_track
        """
        self.execute_script("sqlite_create_tables.sql")

    def add_user(self, id_user: str, username: str, last_name: str, first_name: str):
        self.request(
            f"INSERT INTO users (username, first_name, last_name, id_users) VALUES ("
            f"'{username}', '{first_name}', '{last_name}', '{id_user}'"
            f")"
        )

    def check_user(self, id_user: str, table: str) -> tuple:
        self.request(f"SELECT id_users from {table} WHERE id_users = '{id_user}'")
        return self.cursor.fetchone()

    def request(self, query: str):
        logger.info(f"execute - {query}")
        self.cursor.execute(query)
        self.connect.commit()

    def execute_script(self, script: str):
        with open(f'DataBase/{script}', 'r') as sqlite_file:
            file = sqlite_file.read()
            logger.info(f"Execute script - {file}")
            self.connect.executescript(file)

    def __del__(self):
        logger.info(f"Connect close")
        self.connect.close()
