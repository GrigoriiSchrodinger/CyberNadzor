import logging
import sqlite3

logger = logging.getLogger('root')


class Sqlite:
    def __init__(self, path):
        self.connect = sqlite3.connect(path)
        self.cursor = self.connect.cursor()

    def request(self, query: str, parameters: tuple = ()) -> None:
        logger.info(f"execute - {query}")
        self.cursor.execute(query, parameters)
        self.connect.commit()

    def fetchone(self, query: str, parameters: tuple = ()) -> tuple:
        self.request(query, parameters)
        return self.cursor.fetchone()

    def fetchall(self, query: str, parameters: tuple = ()) -> list[tuple]:
        self.request(query, parameters)
        return self.cursor.fetchall()

    def execute_script(self, script: str) -> None:
        with open(f'src/database/sql_query/{script}', 'r') as sqlite_file:
            file = sqlite_file.read()
            logger.info(f"Execute script - {file}")
            self.connect.executescript(file)

    def __del__(self) -> None:
        logger.info(f"Connect close")
        self.connect.close()


class DataBaseManager(Sqlite):
    GET_USER_DATA_QUERY: str = """
        SELECT
        users.id_users,
        higher_track.'BTC-USD',
        higher_track.'ETH-USD',
        higher_track.'LTC-USD',
        higher_track.'DOGE-USD',
        higher_track.'ADA-USD',
        'higher' AS track_type
    FROM users INNER JOIN higher_track ON higher_track.id = users.id
    UNION ALL
    SELECT
        users.id_users,
        below_track.'BTC-USD',
        below_track.'ETH-USD',
        below_track.'LTC-USD',
        below_track.'DOGE-USD',
        below_track.'ADA-USD',
        'below' AS track_type
    FROM users INNER JOIN below_track ON below_track.id = users.id
    """
    ADD_USER_TO_USER_QUERY = "INSERT INTO users (username, first_name, last_name, id_users) VALUES (?, ?, ?, ?)"
    ADD_USER_TO_BELOW_QUERY = "INSERT INTO below_track (id) VALUES ((SELECT id FROM users WHERE id = ?))"
    ADD_USER_TO_HIGHER_QUERY = "INSERT INTO higher_track (id) VALUES ((SELECT id FROM users WHERE id = ?))"
    CHECK_USER_QUERY = "SELECT id_users from '{}' WHERE id_users = ?"
    UPDATE_CURRENCY_QUERY = "UPDATE '{}' SET '{}'='{}' WHERE id=(SELECT id FROM users WHERE id_users = ?)"
    DELETE_CURRENCY_QUERY = "UPDATE '{}' SET '{}'=NULL WHERE id=(SELECT id FROM users WHERE id_users = ?)"

    def create_tables(self) -> None:
        self.execute_script("sqlite_create_tables.sql")

    def add_user(self, id_user: str, username: str, last_name: str, first_name: str) -> None:
        self.request(self.ADD_USER_TO_USER_QUERY, (username, first_name, last_name, id_user,))
        self.request(self.ADD_USER_TO_BELOW_QUERY, (id_user,))
        self.request(self.ADD_USER_TO_HIGHER_QUERY, (id_user,))

    def get_users_data(self):
        data = {
            'higher': [],
            'below': []
        }

        rows = self.fetchall(self.GET_USER_DATA_QUERY)
        for row in rows:
            user_data = {
                'id_user': row[0],
                'BTC-USD': row[1],
                'ETH-USD': row[2],
                'LTC-USD': row[3],
                'DOGE-USD': row[4],
                'ADA-USD': row[5],
            }

            if row[6] == 'higher':
                data['higher'].append(user_data)
            else:
                data['below'].append(user_data)

        return data

    def check_user(self, id_user: str, table: str) -> tuple:
        return self.fetchone(self.CHECK_USER_QUERY.format(table.replace('"', '""')), (id_user,))

    def update_currency(self, table, currency, quantity, id_user) -> None:
        self.request(self.UPDATE_CURRENCY_QUERY.format(
            table.replace('"', '""'),
            currency.replace('"', '""'),
            quantity),
            (id_user,)
        )

    def delete_currency(self, table, currency, id_user) -> None:
        self.request(self.DELETE_CURRENCY_QUERY.format(
            table.replace('"', '""'),
            currency.replace('"', '""')),
            (id_user,)
        )
