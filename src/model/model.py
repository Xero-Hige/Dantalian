from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
import yaml
import binascii
import datetime
import hashlib
import os
import time
from sqlalchemy.sql.expression import select, exists

EXPIRE_TIME = 60 * 4

Base = declarative_base()

class Users(Base):
    __tablename__ = 'users'
    iduser = Column(Integer, nullable=False, primary_key=True)
    username = Column(String(45), nullable=False, index=True)
    userpass = Column(String(128))
    creation = Column(DateTime, default=datetime.datetime.now, nullable=False)

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

    def __get_token(self):
        user, password, timestamp, userid = self.username, self.userpass, self.creation, self.iduser 
        token_base = user + password + timestamp + userid
        salt = str.encode(userid + timestamp)
        encoded_token = str.encode(token_base)
        hashed = hashlib.pbkdf2_hmac('sha512', encoded_token, salt, 1000)
        hash_hex = binascii.hexlify(hashed)
        return hash_hex.decode("ascii")

    def __init__(self,username):
        if Users.exists(username):
            return None
        self.username = username
        self.password = User.__hash_password(user, user)
        self.creation = User.__get_timestamp() 
        return self.__get_token()

    @staticmethod
    def is_valid_token(user, token):
        users = Users.where(Users.username == user).get()
        for user in users:
            return user.__get_token() == token
        return False

    @staticmethod
    def delete_user(user):
        Users.where(Users.username == user).delete()

    @staticmethod
    def exists(user):
        return Users.where(Users.username == user).count() != 0

class Tag(Base):
    __tablename__ = "tags"
    idtag = Column(Integer, nullable=False, primary_key=True)
    text = Column(String(128))

class Video(Base):
    __tablename__ = "videos"
    idvideo = Column(Integer, nullable=False, primary_key=True)
    name = Column(String(128))


class Gif(Base):
    __tablename__ = "gifs"
    video = relationship(Video)
    idgif = Column(Integer, nullable=False, primary_key=True)
    name = Column(String(128))
    tagged = Column(Boolean())

def get_engine():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    db_yml = os.path.join(dir_path, "db.yml")
    with open(db_yml) as f:
        db_config = yaml.load(f)
    mysql_engine = create_engine('mysql+pymysql://{0}:{1}@127.0.0.1/{2}'.format(db_config["user"], db_config["password"],db_config["schema"]))
    return mysql_engine

if __name__ == "__main__":
    Base.metadata.create_all(get_engine())