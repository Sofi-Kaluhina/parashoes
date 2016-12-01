# coding=utf8

import ujson
from datetime import datetime, timedelta
from tornado import web, gen

from admin.connection import db_session
from admin.model import *


class CORSHandler(web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Credentials", "true")
        self.set_header("Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS")
        self.set_header("Access-Control-Allow-Headers",
                        "Content-Type, Depth, User-Agent, X-File-Size, X-Requested-With, X-Requested-By, If-Modified-Since, X-File-Name, Cache-Control")


class InitHandler(CORSHandler):
    @gen.coroutine
    def get(self, *args, **kwargs):
        result = {}
        query = db_session.query(
            AttributeValue
        ).filter(
            Attribute.name == 'brand',
            ProductAttributeValues is not None
        ).join(
            Attribute,
            Attribute.id == AttributeValue.attribute_id
        ).join(
            ProductAttributeValues,
            ProductAttributeValues.attribute_value_id == AttributeValue.id
        ).all()
        result['brand'] = [
            {
                'name': value.name.encode(),
                'slug_name': value.description
            } for value in query
            ]
        result['categories_filter_conditions'] = {
            'new': {
                'created_at': [(datetime.today() - timedelta(days=3)).strftime('%Y-%m-%d 00:00:00')]
            },
            'woman': {
                'gender': ['Женский']
            },
            'man': {
                'gender': ['Мужской']
            },
            'children': {
                'age': ['Малыши', 'Дети']
            }
        }
        self.write(ujson.dumps(result))

    def post(self, *args, **kwargs):
        self.clear()
        self.set_status(405)

    def put(self, *args, **kwargs):
        self.clear()
        self.set_status(405)

    def delete(self, *args, **kwargs):
        self.clear()
        self.set_status(405)


class HProducts(CORSHandler):
    @staticmethod
    def _get_product_attributes(product_id):
        attributes = db_session.query(
            ProductAttributeValues,
            AttributeValue,
            Attribute
        ).filter(
            ProductAttributeValues.product_id == product_id
        ).join(
            AttributeValue,
            AttributeValue.id == ProductAttributeValues.attribute_value_id
        ).join(
            Attribute,
            Attribute.id == AttributeValue.attribute_id
        ).all()
        result = {}
        for _, attribute_value, attribute in attributes:
            result[attribute.name] = attribute_value.name
        return result

    @staticmethod
    def _get_product_photos(product_id):
        photos = db_session.query(
            ProductsProductPhoto,
            ProductPhoto
        ).filter(
            ProductsProductPhoto.product_id == product_id
        ).join(
            ProductPhoto,
            ProductsProductPhoto.product_photo_id == ProductPhoto.id
        ).all()
        result = []
        for _, photo in photos:
            result.append(
                {
                    'large_name': photo.large_name,
                    'large_path': 'media/product/large/{}'.format(photo.large_path),
                    'small_name': photo.small_name,
                    'small_path': 'media/product/small/{}'.format(photo.small_path),
                    'thumb_name': photo.thumb_name,
                    'thumb_path': 'media/product/thumb/{}'.format(photo.thumb_path),
                }
            )
        return result

    def _get_products(self, products):
        result = []
        for product in products:
            _product = {
                'id': product.id,
                'name': product.name,
                'slug_name': product.slug_name,
                'description': product.description,
                'images': self._get_product_photos(product.id),
                'attributes': self._get_product_attributes(product.id)
            }
            result.append(_product)
        return result


class ProductsHandler(HProducts):
    @gen.coroutine
    def get(self):
        try:
            products = db_session.query(
                Product
            ).all()

            self.write(ujson.dumps(self._get_products(products)))
        except gen.BadYieldError as e:
            self.write(e.args)

    def post(self, *args, **kwargs):
        self.clear()
        self.set_status(405)

    def put(self, *args, **kwargs):
        self.clear()
        self.set_status(405)

    def delete(self, *args, **kwargs):
        self.clear()
        self.set_status(405)


class ProductHandler(HProducts):
    @gen.coroutine
    def get(self, slug_name):
        try:
            products = db_session.query(
                Product
            ).filter(
                Product.slug_name == slug_name
            ).all()

            self.write(ujson.dumps(self._get_products(products)))
        except gen.BadYieldError as e:
            self.write(e.args)

    def post(self, *args, **kwargs):
        self.clear()
        self.set_status(405)

    def put(self, *args, **kwargs):
        self.clear()
        self.set_status(405)

    def delete(self, *args, **kwargs):
        self.clear()
        self.set_status(405)


class CategoriesHandler(HProducts):
    def get(self):
        pass

    @gen.coroutine
    def post(self):
        try:
            def filter_constructor(_conditions):
                result = []
                for condition_list in _conditions:
                    for condition in _conditions[condition_list]:
                        result.append(and_(
                            Attribute.name == condition_list,
                            AttributeValue.name == condition
                        ))
                return result

            conditions = ujson.loads(self.request.body)['categories_filter_conditions']
            products = set()
            _products = db_session.query(
                Product
            ).distinct(
                Product.id
            ).outerjoin(
                ProductAttributeValues,
                Product.id == ProductAttributeValues.product_id
            ).outerjoin(
                AttributeValue,
                ProductAttributeValues.attribute_value_id == AttributeValue.id
            ).outerjoin(
                Attribute,
                AttributeValue.attribute_id == Attribute.id
            ).filter(
                or_(*filter_constructor(conditions))
            ).all()

            for _product in _products:
                products.add(_product)

            self.write(ujson.dumps(self._get_products(products)))
        except TypeError as e:
            self.clear()
            self.set_status(400, reason=str(e))
        except ValueError as e:
            self.clear()
            self.set_status(400, reason=str(e))
        except gen.BadYieldError as e:
            self.write(e.args)

    def put(self, *args, **kwargs):
        self.clear()
        self.set_status(405)

    def delete(self, *args, **kwargs):
        self.clear()
        self.set_status(405)
