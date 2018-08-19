import binascii
import datetime
import hashlib
import time

from base_internalMysql_handler import InternalMysqlHandler
from logger import print_info

EXPIRE_TIME = 60 * 4


class UserHandler(InternalMysqlHandler):
    def __init__(self):
        super().__init__()

    @staticmethod
    def __hash_password(user, password):
        salt = str.encode(user)
        password = str.encode(password)
        iterations = 1200 * len(user)

        hashed = hashlib.pbkdf2_hmac('sha512', password, salt, iterations)
        hash_hex = binascii.hexlify(hashed)
        return hash_hex.decode("ascii")

    @staticmethod
    def __get_timestamp(delta=0):
        ts = time.time()
        timestamp = datetime.datetime.fromtimestamp(ts) + datetime.timedelta(minutes=delta)
        return timestamp.strftime('%Y-%m-%d %H:%M:%S')

    @staticmethod
    def __get_token(password, user, userid, timestamp):
        token_base = user + password + timestamp + userid
        salt = str.encode(userid + timestamp)
        encoded_token = str.encode(token_base)
        hashed = hashlib.pbkdf2_hmac('sha512', encoded_token, salt, 1000)
        hash_hex = binascii.hexlify(hashed)
        return hash_hex.decode("ascii")

    def add_user(self, user):
        cursor = self._get_cursor()

        passwd = self.__hash_password(user, user)

        query = "SELECT iduser FROM users WHERE username='{0}'".format(user)

        cursor.execute(query)
        for _ in cursor:
            return None

        timestamp = self.__get_timestamp()

        query = "INSERT INTO users (username, userpass, created) VALUES ('{0}','{1}','{2}')".format(user,
                                                                                                    passwd,
                                                                                                    timestamp)

        self._get_cursor().execute(query)
        self.connection.commit()

        print_info(__name__, "User {0} created".format(user))

        cursor = self._get_cursor()
        query = (
            "SELECT iduser, username, userpass, created "
            "FROM users "
            "WHERE username = '{}'"
        ).format(user)

        cursor.execute(query)
        iduser, username, userpass, created = cursor[0]
        cursor.close()

        return self.__get_token(userpass, user, iduser, created)

    def is_valid_token(self, user, token):
        cursor = self._get_cursor()

        query = (
            "SELECT iduser, username, userpass, created "
            "FROM users "
            "WHERE username = '{}'"
        ).format(user)

        cursor.execute(query)

        for iduser, username, userpass, created in cursor:
            return self.__get_token(userpass, user, iduser, created) == token

        return False

    def user_exists(self, user):
        cursor = self._get_cursor()

        query = "SELECT iduser FROM users WHERE u.username='{0}'".format(user)

        cursor.execute(query)
        for _ in cursor:
            return True

        return False

    def delete_user(self, user):
        cursor = self._get_cursor()

        query = "DELETE FROM users WHERE username='{0}'".format(user)
        cursor.execute(query)
        self.connection.commit()

        print_info(__name__, "User {0} deleted".format(user))

        cursor.close()
