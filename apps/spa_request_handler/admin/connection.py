# coding=utf8

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tornado.options import options

from admin.model import *

engine = create_engine(options.db_url)
engine.echo = True
session = sessionmaker()
session.configure(bind=engine)
Base.metadata.bind = engine
db_session = session()
