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
from sqlalchemy.sql.expression import func

EXPIRE_TIME = 60 * 4


def get_engine():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    db_yml = os.path.join(dir_path, "db.yml")
    with open(db_yml) as f:
        db_config = yaml.load(f)
    mysql_engine = create_engine('mysql+pymysql://{0}:{1}@{2}/{3}'.format(db_config["user"], db_config["password"], db_config["host"], db_config["schema"]))
    return mysql_engine


def trust_secret_matches(secret):
    with open("trust_secret.yml", "r") as f:
        secret_phrase = yaml.load(f)
    return secret == secret_phrase["secret_phrase"]


db_session = scoped_session(sessionmaker(autocommit=False,
                                         bind=get_engine()))


Base = declarative_base()
Base.query = db_session.query_property()


class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    username = Column(String(45), nullable=False, index=True)
    userpass = Column(String(128))
    creation = Column(DateTime, default=datetime.datetime.now, nullable=False)
    trusted = Column(Boolean(), default=False)

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
    def acknowledge_trusted(username, token, secret):
        if not Users.is_valid_token(username, token):
            return False
        if not trust_secret_matches(secret):
            return False
        user = Users.query.filter(Users.username == username).one()
        user.trusted = True
        db_session.add(user)
        db_session.commit()
        return True

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
    url = Column(String(128))
    category = Column(String(64))
    creation = Column(DateTime, default=datetime.datetime.now, nullable=False)
    filename = Column(String(128))

    def __init__(self, url, category, filename):
        self.url = url
        self.category = category
        self.name = " ".join(url.split("/")[-1].split('-')[:-1])
        self.filename = filename

    @staticmethod
    def create(url, category, filename):
        if Video.exists(url):
            return Video.query.filter(Video.url == url).one().id
        video = Video(url, category, filename)
        db_session.add(video)
        db_session.commit()
        return video.id

    @staticmethod
    def exists(url):
        return Video.query.filter(Video.url == url).count() != 0

    @staticmethod
    def random():
        return Video.query.order_by(func.rand()).first()


class Gif(Base):
    __tablename__ = "gifs"
    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    chunk = Column(Integer)
    creation = Column(DateTime, default=datetime.datetime.now, nullable=False)
    filename = Column(String(128))
    classified = Column(Boolean(), default=False)
    classification = Column(Boolean(), default=None, nullable=True)

    video_id = Column(Integer, ForeignKey('videos.id'))
    video = relationship(Video, backref=backref('gifs', uselist=True))

    tags = relationship("Tag", backref=backref('tags', uselist=True))

    def __init__(self, video_id, chunk, filename):
        self.video_id = video_id
        self.chunk = chunk
        self.filename = filename

    @staticmethod
    def create(video_id, chunk, filename):
        gif = Gif(video_id, chunk, filename)
        db_session.add(gif)
        db_session.commit()
        return gif.id

    @staticmethod
    def random(amnt):
        gifs = Gif.query.order_by(func.rand()).limit(amnt)
        return [gif.id for gif in gifs]

    @staticmethod
    def get(idgif):
        return Gif.query.get(idgif)

    def mark_tagged(self, tag):
        self.classified = True
        self.classification = tag
        db_session.commit()


class TagText(Base):
    __tablename__ = "tagtexts"
    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    text = Column(String(128))

    def __init__(self, text):
        self.text = text

    @staticmethod
    def create(text):
        tagText = TagText(text)
        db_session.add(tagText)
        db_session.commit()
        return tagText.id


class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    result = Column(Boolean())

    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship(Users, backref=backref('users', uselist=True))

    gif_id = Column(Integer, ForeignKey('gifs.id'))
    gif = relationship(Gif, backref=backref('gifs', uselist=True))

    tagtext_id = Column(Integer, ForeignKey('tagtexts.id'))
    tagtext = relationship(TagText, backref=backref('tagtexts', uselist=True))

    def __init__(self, tagtext_id, gif_id, user_id, result):
        self.tagtext_id = tagtext_id
        self.gif_id = gif_id
        self.user_id = user_id
        self.result = result

    @staticmethod
    def create(tagtext_id, gif_id, user_id, result):
        tag = Tag(tagtext_id, gif_id, user_id, result)
        db_session.add(tag)
        db_session.commit()
        return tag.id

    @staticmethod
    def trusted_tag():
        tag = Tag.query.filter(Tag.user.has(trusted=True)).order_by(func.rand()).first()
        return tag


if __name__ == "__main__":
    Base.metadata.create_all(bind=get_engine())
