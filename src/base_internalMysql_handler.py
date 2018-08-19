import sys

from base_mysql_handler import MysqlBaseHandler
from logger import print_error


class InternalMysqlHandler(MysqlBaseHandler):
    def __init__(self):
        super().__init__()

    def open_connection(self):
        try:
            self._open_connection(user='test',
                                  password='test',
                                  database='dantalian',
                                  host='mysql')
        except Exception as e:
            print_error(__name__, str(e))
            print_error(__name__, "Critical: Shutting down")
            sys.exit(11)
