import flask
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session as SessionType
from decouple import config
from distutils.util import strtobool


def is_testing():
    return bool(strtobool(config('testing', default='False')))


def get_db_url():
    testing = is_testing()
    host_db = config('HOST_DB', default=None) if not testing else None
    password_db = config('PASSWORD_DB', default=None) if not testing else None
    user_db = config('USER_DB', default=None) if not testing else None
    database = config('NAME_DB', default=None) if not testing else None
    port_db = config('PORT_DB', default=None) if not testing else None
    return f'postgresql+psycopg2://{user_db}:{password_db}@{host_db}:{port_db}/{database}' \
        if not testing \
        else 'sqlite:///file.db'


def get_engine():
    url_db = get_db_url()
    return create_engine(url_db, pool_size=20)


def get_session() -> SessionType:
    g = flask.g
    """ if 'session' not in g:
        engine = get_engine()
        Session = scoped_session(sessionmaker(engine))
        #Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        session: SessionType = Session()
        g.session = session """
    return g.session


Base = declarative_base()

CMG_AUTH_URL = config("CMG_AUTH_URL")
