# coding=utf8

from flask import Flask
from flask_admin import Admin

app = Flask(__name__)

admin = Admin(app, name='BUlavka', template_mode='bootstrap3')
