# coding=utf8

import os
import sys
from flask import Flask
from flask_babelex import Babel
from flask import session, request
from tornado.options import options

app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if "db_url" not in options.as_dict().keys():
    sys.path.append(os.path.dirname(BASE_DIR))

    from options import load_options

    load_options()
    from admin.connection import db_session

babel = Babel(app)


@babel.localeselector
def get_locale():
    if request.args.get('lang'):
        session['lang'] = request.args.get('lang')
    return session.get('lang', 'ru')
