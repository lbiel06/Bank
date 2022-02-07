import sqlite3


FILE = 'database.db'


def execute_sql_query(query: str, parameters: tuple = ()) -> None:
    with sqlite3.connect(FILE) as connection:
        connection.cursor().execute(query, parameters)


def setup() -> None:
    execute_sql_query('CREATE TABLE users (username TEXT, password TEXT, balance INTEGER)')


class User:
    @staticmethod
    def register(username: str, password: str) -> None:
        execute_sql_query('INSERT INTO users VALUES(?, ?, 0)', (username, password))

    @staticmethod
    def remove(username: str) -> None:
        execute_sql_query('DELETE FROM users WHERE username=?', (username,))

    @staticmethod
    def set_balance(username: str, balance: int) -> None:
        execute_sql_query('UPDATE users SET balance=? WHERE username=?', (balance, username))

    @staticmethod
    def find(username: str) -> tuple:
        with sqlite3.connect(FILE) as connection:
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM users WHERE username=?', (username,))
            return cursor.fetchone()


if __name__ == '__main__':
    setup()
