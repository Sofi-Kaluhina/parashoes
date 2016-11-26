# coding=utf8

import flask_login
from flask import url_for, redirect, request
from flask_admin import helpers, expose, AdminIndexView
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import form, fields, validators

from admin import app, db_session
from admin.model import *


def init_login():
    """
    Initialize flask-login

    :return:
    """
    login_manager = flask_login.LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        """
        Create user loader function
        :param user_id:
        :return:
        """
        return db_session.query(User).get(user_id)


init_login()


class LoginForm(form.Form):
    """
    Define login and registration forms (for flask-login)
    """
    username = fields.StringField(validators=[validators.required()])
    password = fields.PasswordField(validators=[validators.required()])

    def validate_username(self, field):
        """
        we're comparing the plaintext pw with the the hash from the db
        to compare plain text passwords use
        >>>if user.password != self.password.data:
        :param field:
        :type field: object
        :return: None
        """
        user = self.get_user()

        if user is None:
            raise validators.ValidationError('Invalid user')

        if not check_password_hash(user.password, self.password.data):
            raise validators.ValidationError('Invalid password')

        user = db_session.query(User).filter(
            User.username == self.username.data
        ).first()
        user.last_login_at = datetime.now()
        db_session.flush()

    def get_user(self):
        """
        Method for getting user
        :return: None
        """
        return db_session.query(User).filter_by(username=self.username.data).first()


class RegistrationForm(form.Form):
    username = fields.StringField(validators=[validators.required()])
    email = fields.StringField()
    password = fields.PasswordField(validators=[validators.required()])

    def validate_username(self, field):
        if db_session.query(User).filter_by(username=self.username.data).count() > 0:
            raise validators.ValidationError('Duplicate username')


class MyAdminIndexView(AdminIndexView):
    """
    Create customized index view class that handles login & registration
    """

    @expose('/')
    def index(self):
        if not flask_login.current_user.is_authenticated:
            return redirect(url_for('.login_view'))
        return super(MyAdminIndexView, self).index()

    @expose('/login/', methods=('GET', 'POST'))
    def login_view(self):
        """
        handle user login

        :return: object
        """
        form = LoginForm(request.form)
        if helpers.validate_form_on_submit(form):
            user = form.get_user()
            flask_login.login_user(user)

        if flask_login.current_user.is_authenticated:
            return redirect(url_for('.index'))
        link = '<p>Don\'t have an account? <a href="' + url_for('.register_view') + '">Click here to register.</a></p>'
        self._template_args['form'] = form
        self._template_args['link'] = link
        return super(MyAdminIndexView, self).index()

    @expose('/register/', methods=('GET', 'POST'))
    def register_view(self):
        """
        we hash the users password to avoid saving it as plaintext in the db,
        remove to use plain text:

        :return: object
        """
        form = RegistrationForm(request.form)
        if helpers.validate_form_on_submit(form):
            user = User()

            form.populate_obj(user)
            user.password = generate_password_hash(form.password.data)

            db_session.add(user)
            db_session.commit()

            flask_login.login_user(user)
            return redirect(url_for('.index'))
        link = '<p>Already have an account? <a href="' + url_for('.login_view') + '">Click here to log in.</a></p>'
        self._template_args['form'] = form
        self._template_args['link'] = link
        return super(MyAdminIndexView, self).index()

    @expose('/logout/')
    def logout_view(self):
        flask_login.logout_user()
        return redirect(url_for('.index'))
