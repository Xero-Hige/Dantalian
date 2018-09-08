from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship, backref
import yaml
import binascii
import datetime
import hashlib
import os
import time


EXPIRE_TIME = 60 * 4


def get_engine():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    db_yml = os.path.join(dir_path, "db.yml")
    with open(db_yml) as f:
        db_config = yaml.load(f)
    mysql_engine = create_engine('mysql+pymysql://{0}:{1}@{2}/{3}'.format(db_config["user"], db_config["password"], db_config["host"], db_config["schema"]))
    return mysql_engine


db_session = scoped_session(sessionmaker(autocommit=False,
                                         bind=get_engine()))


Base = declarative_base()
Base.query = db_session.query_property()


class Users(Base):
    __tablename__ = 'users'
    # I don't _actually_ need this but for sqlalchemy to stop complaining
    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
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

    def __init__(self, username):
        self.username = username
        self.userpass = Users.__hash_password(username, username)
        self.creation = Users.__get_timestamp()

    @staticmethod
    def create(username):
        if Users.exists(username):
            return None
        user = Users(username)
        db_session.add(user)
        db_session.commit()
        return user.__get_token()

    @staticmethod
    def is_valid_token(user, token):
        users = Users.where(Users.username == user).one()
        for user in users:
            return user.__get_token() == token
        return False

    @staticmethod
    def delete_user(user):
        Users.query.filter(Users.username == user).delete()
        db_session.commit()

    @staticmethod
    def exists(user):
        return Users.query.filter(Users.username == user).count() != 0

    def __get_token(self):
        user, password, timestamp = self.username, self.userpass, self.creation.isoformat()
        token_base = user + password + str(timestamp)
        salt = str.encode(timestamp)
        encoded_token = str.encode(token_base)
        hashed = hashlib.pbkdf2_hmac('sha512', encoded_token, salt, 1000)
        hash_hex = binascii.hexlify(hashed)
        return hash_hex.decode("ascii")


class Video(Base):
    __tablename__ = "videos"
    id = Column(Integer, nullable=False, primary_key=True)
    name = Column(String(128))


class Gif(Base):
    __tablename__ = "gifs"
    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    name = Column(String(128))
    tagged = Column(Boolean())

    video_id = Column(Integer, ForeignKey('videos.id'))
    video = relationship(Video, backref=backref('gifs', uselist=True))


class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    text = Column(String(128))
    result = Column(Boolean())

    gif_id = Column(Integer, ForeignKey('gifs.id'))
    gif = relationship(Gif, backref=backref('gifs', uselist=True))


if __name__ == "__main__":
    Base.metadata.create_all(bind=get_engine())
