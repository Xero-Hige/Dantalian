import mysql.connector

from base_db_handler import DbBaseHandler


class MysqlBaseHandler(DbBaseHandler):
    def __init__(self):
        super().__init__()
        self.connection = None

    def _open_connection(self, user, password, database, host):
        self.connection = mysql.connector.connect(user=user,
                                                  database=database,
                                                  password=password,
                                                  host=host)

    def close_connection(self):
        self.connection.close()

    def _get_cursor(self):
        if not self.connection:
            self.open_connection()

        try:
            return self.connection.cursor()
        except Exception:
            self.open_connection()
            return self.connection.cursor()
