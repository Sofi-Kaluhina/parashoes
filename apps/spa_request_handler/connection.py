#coding=utf8

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tornado.options import options

from model import *


engine = create_engine(options.db_url)
session = sessionmaker()
session.configure(bind=engine)
Base.metadata.bind = engine
s = session()