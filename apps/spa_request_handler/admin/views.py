# coding=utf8

import os
from datetime import datetime

from flask import url_for
from flask_admin import form
from flask_admin.contrib.sqla import ModelView
from slugify import slugify_url
from jinja2 import Markup
from wtforms import StringField, IntegerField, DateTimeField, SelectField

from admin import app, db_session, options
from admin.model import *
from admin.security import flask_login


class UserView(ModelView):
    def __init__(self, session, **kwargs):
        self.can_delete = False
        self.can_export = True
        self.create_modal = True
        self.edit_modal = True
        self.column_exclude_list = ['password', ]
        self.form_excluded_columns = ['password', ]
        super().__init__(User, session, **kwargs)

    def is_accessible(self):
        return flask_login.current_user.is_authenticated


class CatalogUserTypeView(ModelView):
    def __init__(self, session, **kwargs):
        super().__init__(CatalogUserType, session, **kwargs)

    def is_accessible(self):
        return flask_login.current_user.is_authenticated


class ProductPhotoView(ModelView):
    def __init__(self, session, **kwargs):
        self.create_modal = True
        self.edit_modal = True
        super().__init__(ProductPhoto, session, **kwargs)

    def is_accessible(self):
        return flask_login.current_user.is_authenticated

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


class AttributeView(ModelView):
    def __init__(self, session, **kwargs):
        super().__init__(Attribute, session, **kwargs)

    def is_accessible(self):
        return flask_login.current_user.is_authenticated


class AttributeValueView(ModelView):
    def __init__(self, session, **kwargs):
        super().__init__(AttributeValue, session, **kwargs)

    def is_accessible(self):
        return flask_login.current_user.is_authenticated


class ProductView(ModelView):
    def __init__(self, session, **kwargs):
        self.name = 'Товары'
        self.create_modal = False
        self.edit_modal = False
        self.can_view_details = True
        self.can_edit = False
        self.can_export = True
        self.column_exclude_list = ['slug_name', ]
        self.form_excluded_columns = ['slug_name', ]
        self.on_form_prefill(self.form, None)
        super(ProductView, self).__init__(Product, session, **kwargs)
        self._refresh_cache()
        self.on_form_prefill(self.form, self.model.id)

    def is_accessible(self):
        return flask_login.current_user.is_authenticated

    def on_form_prefill(self, form, id):
        self.form_extra_fields = {}
        disables = {}
        for attribute in db_session.query(Attribute).all():
            if attribute.type == 'integer':
                self.form_extra_fields[attribute.name] = IntegerField(
                    default=self._get_price_value(id)
                )
            elif attribute.type == 'string':
                self.form_extra_fields[attribute.name] = StringField()
            elif attribute.type == 'datetime':
                self.form_extra_fields[attribute.name] = DateTimeField(
                    default=self._get_created_at_value(id)
                )
            elif attribute.type == 'select':
                self.form_extra_fields[attribute.name] = SelectField(
                    coerce=int,
                    choices=self._get_selectable_field_choices(attribute.id)
                )
            elif attribute.type == 'string_auto':
                self.form_extra_fields[attribute.name] = StringField(
                    default=self._get_new_oem_value(id)
                )
            disables[attribute.name] = {'disabled': not attribute.is_active}

        self.form_widget_args = disables

    def on_model_change(self, form, model, is_created):
        model.slug_name = slugify_url(form['name'].data)
        if is_created:
            for attribute in db_session.query(Attribute).all():
                if attribute.name == 'created_at':
                    attribute_created_at_insert = (
                        AttributeValue(
                            attribute_id=attribute.id,
                            name=self._get_created_at_value(model.id).strftime('%Y-%m-%d %H:%M:%S'),
                            description=self._get_created_at_value(model.id).strftime('%Y-%m-%d %H:%M:%S')
                        )
                    )
                    db_session.add(attribute_created_at_insert)
                    db_session.flush()
                    db_session.refresh(attribute_created_at_insert)
                    product_attribute_created_at_insert = (
                        ProductAttributeValues(
                            product_id=model.id,
                            attribute_value_id=attribute_created_at_insert.id
                        )
                    )
                    db_session.add(product_attribute_created_at_insert)
                    db_session.flush()
                elif attribute.name == 'oem':
                    attribute_new_oem_insert = (
                        AttributeValue(
                            attribute_id=attribute.id,
                            name=self._get_new_oem_value(model.id),
                            description=self._get_new_oem_value(model.id)
                        )
                    )
                    db_session.add(attribute_new_oem_insert)
                    db_session.flush()
                    db_session.refresh(attribute_new_oem_insert)
                    product_attribute_new_oem_insert = (
                        ProductAttributeValues(
                            product_id=model.id,
                            attribute_value_id=attribute_new_oem_insert.id
                        )
                    )
                    db_session.add(product_attribute_new_oem_insert)
                    db_session.flush()
                elif attribute.name == 'price':
                    attribute_new_oem_insert = (
                        AttributeValue(
                            attribute_id=attribute.id,
                            name=form[attribute.name].data,
                            description=form[attribute.name].data
                        )
                    )
                    db_session.add(attribute_new_oem_insert)
                    db_session.flush()
                    db_session.refresh(attribute_new_oem_insert)
                    product_attribute_new_oem_insert = (
                        ProductAttributeValues(
                            product_id=model.id,
                            attribute_value_id=attribute_new_oem_insert.id
                        )
                    )
                    db_session.add(product_attribute_new_oem_insert)
                    db_session.flush()
                else:
                    product_attribute_selectable_insert = (
                        ProductAttributeValues(
                            product_id=model.id,
                            attribute_value_id=form[attribute.name].data
                        )
                    )
                    db_session.add(product_attribute_selectable_insert)
                    db_session.flush()
        else:
            pass

    def on_model_delete(self, model):
        product_attribute_values_delete = db_session.query(
            ProductAttributeValues
        ).filter(
            ProductAttributeValues.product_id == model.id
        ).all()

        attribute_value_ids = db_session.query(
            ProductAttributeValues.attribute_value_id
        ).filter(
            ProductAttributeValues.product_id == model.id,
            Attribute.type != 'select'
        ).join(
            AttributeValue,
            AttributeValue.id == ProductAttributeValues.attribute_value_id
        ).join(
            Attribute,
            Attribute.id == AttributeValue.attribute_id
        ).all()

        for product_attribute_value_delete in product_attribute_values_delete:
            db_session.delete(product_attribute_value_delete)

        attribute_values_delete = db_session.query(
            AttributeValue
        ).filter(
            AttributeValue.id.in_(attribute_value_ids)
        ).all()

        for attribute_value_delete in attribute_values_delete:
            db_session.delete(attribute_value_delete)

        db_session.flush()

    def _get_attribute_value(self, attribute_name, id):
        return db_session.query(
            AttributeValue
        ).filter(
            Attribute.name == attribute_name,
            Product.id == id
        ).join(
            Attribute,
            Attribute.id == AttributeValue.attribute_id
        ).join(
            ProductAttributeValues,
            ProductAttributeValues.attribute_value_id == AttributeValue.id
        ).join(
            Product,
            Product.id == ProductAttributeValues.product_id
        ).first()

    def _get_created_at_value(self, id):
        result = self._get_attribute_value('created_at', id)
        if result:
            return datetime.today().strptime(result.name, '%Y-%m-%d %H:%M:%S')
        else:
            return datetime.today()

    def _get_new_oem_value(self, id):
        result = self._get_attribute_value('oem', id)
        if result:
            return result.name
        else:
            last_product_id = db_session.query(
                Product
            ).order_by(
                desc(
                    Product.id
                )
            ).limit(1).first()
            return 'BU{:05d}'.format(last_product_id.id)

    def _get_price_value(self, id):
        result = self._get_attribute_value('price', id)
        if result:
            return result.name
        else:
            return 0

    def _get_selectable_field_choices(self, id):
        choices = [
            (c.id, c.name) for c in db_session.query(
                    AttributeValue
                ).filter(
                    AttributeValue.attribute_id == id
                ).all()
            ]
        return choices
