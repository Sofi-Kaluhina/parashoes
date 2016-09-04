# coding=utf8
import os
import sys
from jinja2 import Markup

from flask import Flask, url_for
from flask import request
from flask import session
from flask_admin import Admin, form
from flask_admin.contrib.sqla import ModelView
from flask_admin.model import BaseModelView
from flask_babelex import Babel
# import flask_login as login
# from slugify import slugify # for slugify product name

from tornado.options import options
from model import *


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if "db_url" not in options.as_dict().keys():
    sys.path.append(os.path.dirname(BASE_DIR))

    from options import load_options

    load_options()

    from connection import db_session

app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

#############################
#### Admin panel localisation

babel = Babel(app)

@babel.localeselector
def get_locale():
    if request.args.get('lang'):
        session['lang'] = request.args.get('lang')
    return session.get('lang', 'ru')

############################


class UserView(ModelView):
    can_delete = False
    can_export = True
    create_modal = True
    edit_modal = True
    column_exclude_list = ['password', ]
    column_details_exclude_list = ['password', ]


class AddNewProduct(ModelView):
    create_modal = True
    edit_modal = True

    @app.route('/media/product/<filename>')
    def product_image(self):
        pass

    @app.route('/media/product/thumb/<filename>')
    def product_trumb_image(self):
        pass

    def _list_thumbnail(view, context, model, name):
        if not model.path:
            return ''

        return Markup('<img src="%s">' % url_for(
            'product_trumb_image',
            filename=form.thumbgen_filename(model.path))
        )

    def thumb_name(filename):
        return 'thumb/%s_thumb%s' % os.path.splitext(filename)

    column_formatters = {
        'path': _list_thumbnail,
        'thumb_path': _list_thumbnail
    }


    form_extra_fields = {
        'path': form.ImageUploadField(
            'Path',
            base_path='{}/{}'.format(options.as_dict()['media_dir'], 'product'),
            thumbgen=thumb_name,
            thumbnail_size=(100, 100, True),
            endpoint='product_image'
        )
    }

admin = Admin(app, name='BUlavka', template_mode='bootstrap3')
admin.add_view(UserView(User, db_session))
admin.add_view(ModelView(CatalogUserType, db_session))

admin.add_view(AddNewProduct(ProductPhoto, db_session))

admin.add_view(ModelView(Product, db_session))
admin.add_view(ModelView(CatalogProductAttribute, db_session))

