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
        """
        with open('DataBase/sqlite_create_tables.sql', 'r') as sqlite_file:
            sql_script = sqlite_file.read()

        self.connect.executescript(sql_script)

    def add_users(self, id_user: str, username: str, last_name: str, first_name: str):
        try:
            self.request(
                f"INSERT INTO users (username, first_name, last_name, id_users) VALUES ("
                f"'{username}', '{first_name}', '{last_name}', '{id_user}'"
                f")"
            )
        except sqlite3.IntegrityError as error:
            logger.debug(error)
            logger.info(f"Пользователь {id_user} уже есть в базе")

    def request(self, query):
        self.cursor.execute(query)
        logger.info(f"execute - {query}")
        self.connect.commit()

    def __del__(self):
        logger.info(f"Connect close")
        self.connect.close()
