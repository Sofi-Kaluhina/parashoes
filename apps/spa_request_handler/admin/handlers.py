# coding=utf8

import ujson
from datetime import datetime, timedelta
from tornado import web, gen

from admin.connection import db_session
from admin.model import *
from sqlalchemy.exc import IntegrityError


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
        user_id = self.get_argument('user_id')
        self.set_status(200, reason='User with user_id {user_id} successfully created.'.format(user_id=user_id))
        self.write(ujson.dumps(result))

    def put(self, *args, **kwargs):
        result = []
        user_id = self.get_argument('user_id')
        self.set_status(200, reason='User with user_id {user_id} successfully updated.'.format(user_id=user_id))
        self.write(ujson.dumps(result))

    def delete(self, *args, **kwargs):
        user_id = self.get_argument('user_id')
        try:
            user = db_session.query(
                User
            ).filter(
                User.id == user_id
            ).one()
            db_session.delete(user)
            db_session.commit()
            result = {
                'message': 'User with user_id {user_id} successfully deleted.'.format(user_id=user_id)
            }
            self.set_status(200, reason=result['message'])
            self.write(ujson.dumps(result))
        except IntegrityError as e:
            db_session.rollback()
            db_session.commit()
            result = {
                'message': 'User with user_id {user_id} not deleted due to {reason}'.format(
                    user_id=user_id,
                    reason=str(e.args)
                )
            }
            self.set_status(200, reason=result['message'])
            self.write(ujson.dumps(result))
        except gen.BadYieldError as e:
            self.write(e.args)

    def options(self):
        self.set_status(204)
        self.finish()