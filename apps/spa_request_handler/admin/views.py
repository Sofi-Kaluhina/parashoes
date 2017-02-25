# coding=utf8

import os
from datetime import datetime
from PIL import Image
from uuid import uuid4 as uuid

from flask import url_for
from flask_admin import form as flask_form
from flask_admin.contrib.sqla import ModelView
from slugify import slugify_url, UniqueSlugify

from jinja2 import Markup
from wtforms import StringField, IntegerField, DateTimeField, SelectField, FieldList

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
        self.name = 'Пользователи'

    def is_accessible(self):
        return flask_login.current_user.is_authenticated


class CatalogUserTypeView(ModelView):
    def __init__(self, session, **kwargs):
        super().__init__(CatalogUserType, session, **kwargs)
        self.name = 'Типы пользователей'

    def is_accessible(self):
        return flask_login.current_user.is_authenticated


class ProductPhotoView(ModelView):
    def __init__(self, session, **kwargs):
        self.create_modal = True
        self.edit_modal = True
        self.column_exclude_list = ['large_name', 'large_path', 'small_name', 'small_path']
        self.form_excluded_columns = ['large_name', 'large_path', 'small_name', 'small_path', 'thumb_name', 'thumb_path']
        super().__init__(ProductPhoto, session, **kwargs)
        self.name = 'Фотографии товаров'

    def is_accessible(self):
        return flask_login.current_user.is_authenticated

    @app.route('/media/product/large/<filename>')
    def product_image(self):
        pass

    @app.route('/media/product/thumb/<filename>')
    def product_trumb_image(self):
        pass

    def _list_thumbnail(view, context, model, name):
        if not model.large_path:
            return ''

        return Markup('<img src="%s">' % url_for(
            'product_trumb_image',
            filename=flask_form.thumbgen_filename(model.large_path.replace('_large', '')))
        )

    def on_model_change(self, form, model, is_created):
        if is_created:
            size_large = 1035, 1440
            size_small = 414, 576
            size_thumb = 93, 129
            new_photo_file_name = uuid()

            def delete(source_file_name):
                source_directory = '{}/{}/{}'.format(
                    options.as_dict()['media_dir'],
                    'product/large',
                    source_file_name
                )
                os.remove(source_directory)

            def resize(size, destination, source_file_name):
                filename, extension = os.path.splitext(source_file_name)
                source_directory = '{}/{}/{}'.format(
                    options.as_dict()['media_dir'],
                    'product/large',
                    source_file_name
                )
                destination_file = '{}_{}{}'.format(
                    new_photo_file_name,
                    destination,
                    extension
                )
                destination_directory = '{}/{}/{}/{}'.format(
                    options.as_dict()['media_dir'],
                    'product',
                    destination,
                    destination_file
                )
                if source_file_name != destination:
                    try:
                        im = Image.open(source_directory)
                        im.thumbnail(size, Image.ANTIALIAS)
                        im.save(destination_directory, "JPEG")
                    except IOError as e:
                        print(e)
                        print("Cannot create thumbnail for '%s'" % model.large_path)
                return destination_file

            temp_photo_file_name = model.large_path

            large_file_mane = resize(size_large, 'large', temp_photo_file_name)
            small_file_mane = resize(size_small, 'small', temp_photo_file_name)
            thumb_file_mane = resize(size_thumb, 'thumb', temp_photo_file_name)

            delete(temp_photo_file_name)

            def get_unique_product_name():
                counter = 0
                while 1:
                    if db_session.query(exists().where(ProductPhoto.large_name == '{}_{}'.format(model.product[0].name, counter))).scalar():
                        counter += 1
                    else:
                        return '{}_{}'.format(model.product[0].name, counter)

            print('\n', get_unique_product_name(), '\n')

            model.large_name = get_unique_product_name()
            model.large_path = large_file_mane
            model.small_name = model.large_name
            model.small_path = small_file_mane
            model.thumb_name = model.large_name
            model.thumb_path = thumb_file_mane

    def on_model_delete(self, model):
        for destination in ['large', 'small', 'thumb']:
            infile = model.large_path\
                .replace('_large', '')
            filename, extension = os.path.splitext(infile)
            image_file = '{media_dir}/{type_entity_dir}/{destination}/{filename}_{destination}{extension}'.format(
                media_dir=options.as_dict()['media_dir'],
                type_entity_dir='product',
                destination=destination,
                filename=filename,
                extension=extension
            )
            os.remove(image_file)

    column_formatters = {
        'large_path': _list_thumbnail,
        'thumb_path': _list_thumbnail
    }

    form_extra_fields = {
        'large_path': flask_form.ImageUploadField(
            'Path',
            base_path='{}/{}'.format(options.as_dict()['media_dir'], 'product/large'),
            endpoint='product_image'
        )
    }


class AttributeView(ModelView):
    def __init__(self, session, **kwargs):
        super().__init__(Attribute, session, **kwargs)
        self.name = 'Аттрибуты'

    def is_accessible(self):
        return flask_login.current_user.is_authenticated


class AttributeValueView(ModelView):
    def __init__(self, session, **kwargs):
        super().__init__(AttributeValue, session, **kwargs)
        self.name = 'Значения аттрибутов'

    def is_accessible(self):
        return flask_login.current_user.is_authenticated


class ProductTypeView(ModelView):
    def __init__(self, session, **kwargs):
        super().__init__(ProductType, session, **kwargs)
        self.name = 'Типы товаров'

    def is_accessible(self):
        return flask_login.current_user.is_authenticated


class ProductView(ModelView):
    def __init__(self, session, **kwargs):
        self.create_modal = False
        self.edit_modal = False
        self.can_view_details = True
        self.can_edit = False
        self.can_export = True
        self.slug_names = self._get_all_slug_names()
        self.column_exclude_list = ['slug_name', 'filters']
        self.form_excluded_columns = ['slug_name', 'filters']
        self.on_form_prefill(self.form, None)
        super(ProductView, self).__init__(Product, session, **kwargs)
        self._refresh_cache()
        self.name = 'Товары'

    def is_accessible(self):
        return flask_login.current_user.is_authenticated

    def on_form_prefill(self, form, id):
        self.form_extra_fields = {}
        disables = {}
        for attribute in db_session.query(Attribute).all():
            print(attribute.name, attribute.type)
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
            elif attribute.type == 'select_create':
                self.form_extra_fields[attribute.name] = SelectField(
                    coerce=int,
                    choices=self._get_selectable_field_choices(attribute.id)
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

        if is_created:
            model.slug_name = self._get_unique_slug(form['name'].data.lower())
            filters = []
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
                    filters.append(product_attribute_created_at_insert.id)
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
                    filters.append(product_attribute_new_oem_insert.id)
                    db_session.add(product_attribute_new_oem_insert)
                    db_session.flush()
                elif attribute.name == 'price':
                    attribute_price_insert = (
                        AttributeValue(
                            attribute_id=attribute.id,
                            name=form[attribute.name].data,
                            description=form[attribute.name].data
                        )
                    )
                    db_session.add(attribute_price_insert)
                    db_session.flush()
                    db_session.refresh(attribute_price_insert)
                    product_attribute_price_insert = (
                        ProductAttributeValues(
                            product_id=model.id,
                            attribute_value_id=attribute_price_insert.id
                        )
                    )
                    db_session.add(product_attribute_price_insert)
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
            attribute_value_ids = db_session.query(
                ProductAttributeValues.attribute_value_id
            ).filter(
                ProductAttributeValues.product_id == model.id
            ).join(
                AttributeValue,
                AttributeValue.id == ProductAttributeValues.attribute_value_id
            ).join(
                Attribute,
                Attribute.id == AttributeValue.attribute_id
            ).all()
            model.filters = [i[0] for i in attribute_value_ids]

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
            Attribute.type != 'select',
            Attribute.type != 'select_create'
        ).join(
            AttributeValue,
            AttributeValue.id == ProductAttributeValues.attribute_value_id
        ).join(
            Attribute,
            Attribute.id == AttributeValue.attribute_id
        ).all()

        for product_attribute_value_delete in product_attribute_values_delete:
            db_session.delete(product_attribute_value_delete)
        db_session.flush()

        attribute_values_delete = db_session.query(
            AttributeValue
        ).filter(
            AttributeValue.id.in_(attribute_value_ids),
        ).all()

        for attribute_value_delete in attribute_values_delete:
            db_session.delete(attribute_value_delete)
        db_session.flush()

        products_product_photos_delete = db_session.query(
            ProductsProductPhoto
        ).filter(
            ProductsProductPhoto.product_id == model.id
        ).all()

        for products_product_photo_delete in products_product_photos_delete:
            db_session.delete(products_product_photo_delete)
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
        try:
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
        except AttributeError:
            return 'BU{:05d}'.format(1)

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

    def _get_all_slug_names(self):
        return db_session.query(
            Product.slug_name
        ).all()

    def _get_unique_slug(self, product_name):
        slugify_unique = UniqueSlugify(separator='-')
        _slug = slugify_unique(product_name)
        while _slug in [i[0] for i in self.slug_names]:
            _slug = slugify_unique(product_name)
        else:
            slugify_unique = UniqueSlugify(separator='-')
            return _slug
