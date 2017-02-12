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
                        'id': user.id,
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
        print(ujson.loads(self.request.body))
        args = ujson.loads(self.request.body)
        args['is_created'] = False if 'is_created' not in args else args['is_created']
        try:
            new_user = User(**args)
            db_session.add(new_user)
            db_session.commit()
            self.set_status(200, reason='User with login {login} successfully created.'.format(login=args['username']))
            self.write(ujson.dumps(result))
        except IntegrityError as e:
            db_session.rollback()
            db_session.commit()
            self.set_status(200, reason='User with login {login} can not be create. Reason: {reason}'.format(
                login=args['username'],
                reason=str(e.args)
            ))
            self.write(ujson.dumps(result))

    def put(self, *args, **kwargs):
        result = []
        user_id = self.get_argument('user_id')
        self.set_status(200, reason='User with login {login} successfully updated.'.format(login=user_id))
        self.write(ujson.dumps(result))

    def delete(self, *args, **kwargs):
        result = []
        user_id = self.get_argument('user_id')
        user = db_session.query(
            User
        ).filter(
            User.id == user_id
        ).one()
        try:
            db_session.delete(user)
            db_session.commit()
            self.set_status(200, reason='User with login {login} successfully deleted.'.format(login=user.username))
            self.write(ujson.dumps(result))
        except IntegrityError as e:
            db_session.rollback()
            db_session.commit()
            self.set_status(200, reason='User with login {login} can not be delete. Reason: {reason}'.format(
                login=user.username,
                reason=str(e.args)
            ))
            self.write(ujson.dumps(result))

    def options(self):
        self.set_status(204)
        self.finish()