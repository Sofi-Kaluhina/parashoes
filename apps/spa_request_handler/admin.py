# coding=utf8
import os
import sys

from flask import Flask
from flask import request
from flask import session
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from tornado.options import options

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if "db_url" not in options.as_dict().keys():
    sys.path.append(os.path.dirname(BASE_DIR))

    from options import load_options

    load_options()

from model import *
from connection import db_session
from flask_babelex import Babel

app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

babel = Babel(app)

@babel.localeselector
def get_locale():
    if request.args.get('lang'):
        session['lang'] = request.args.get('lang')
    return session.get('lang', 'ru')

admin = Admin(app, name='BUlavka', template_mode='bootstrap3')
admin.add_view(ModelView(User, db_session))
admin.add_view(ModelView(CatalogUserType, db_session))
