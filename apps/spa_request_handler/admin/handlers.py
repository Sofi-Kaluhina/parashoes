# coding=utf8

import ujson
from datetime import datetime, timedelta
from tornado import web, gen

from admin.connection import db_session
from admin.model import *


class CORSHandler(web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS, DELETE, PUT")
        self.set_header("Access-Control-Max-Age", "1000")
        self.set_header("Access-Control-Allow-Headers",
                        "x-requested-with, Content-Type, origin, authorization, accept, client-security-token")


class AdminUser(CORSHandler):
    def get(self, *args, **kwargs):
        try:
            result = []
            users = db_session.query(
                User
            ).all()
            for user in users:
                result.append(
                    {
                        'login': user.username,
                        'firstname': user.firstname,
                        'lastname': user.lastname,
                        'gender': '',
                        'email': user.email,
                        'created_at': user.created_at.isoformat(),
                        'last_login_at': user.last_login_at.isoformat(),
                    }
                )
            self.write(ujson.dumps(result))
        except gen.BadYieldError as e:
            self.write(e.args)

    def post(self, *args, **kwargs):
        result = []
        login = self.get_argument('login')
        self.set_status(200, reason='User with login {login} successfully created.'.format(login=login))
        self.write(ujson.dumps(result))

    def put(self, *args, **kwargs):
        result = []
        login = self.get_argument('login')
        self.set_status(200, reason='User with login {login} successfully updated.'.format(login=login))
        self.write(ujson.dumps(result))

    def delete(self, *args, **kwargs):
        result = []
        login = self.get_argument('login')
        self.set_status(200, reason='User with login {login} successfully deleted.'.format(login=login))
        self.write(ujson.dumps(result))

    def options(self):
        self.set_status(204)
        self.finish()