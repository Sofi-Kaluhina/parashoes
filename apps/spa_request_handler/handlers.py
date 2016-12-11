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
        result = {
            'brand': {},
            'categories_filter_conditions': {}
        }
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
        for value in query:
            result['categories_filter_conditions'][value.description] = [value.id]
        result['categories_filter_conditions'].update(
            {
                'new': [(datetime.today() - timedelta(days=3)).strftime('%Y-%m-%d 00:00:00')],
                'woman': [79],
                'man': [78],
                'children': [28]
            }
        )
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

    @staticmethod
    def _get_filters(filters):
        result = []
        _filters = []
        for filter in filters:
            _filter = {
                'attribute_name': filter[0].name,
                'attribute_value_id': filter[1].id,
                'attribute_value': filter[1].name,
            }
            _filters.append(_filter)
        attribute_names = set(i['attribute_name'] for i in _filters)
        attribute_value = []
        filter_exclude = ['created_at', 'oem']
        for attribute_name in attribute_names:
            if attribute_name not in filter_exclude:
                for filter in _filters:
                    if filter['attribute_name'] == attribute_name:
                        attribute_value.append({
                            'id': filter['attribute_value_id'],
                            'value': filter['attribute_value']
                        })
                if len(attribute_value) > 1:
                    result.append({
                        'filter_name': attribute_name,
                        'filter_value': attribute_value
                    })
                attribute_value = []
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
            conditions = ujson.loads(self.request.body)['categories_filter_conditions']
            filters = set()
            result = {}

            for i in conditions:
                if not isinstance(i, int):
                    raise TypeError('One or more filter items is not integer')
            if len(conditions) == 0:
                raise ValueError('Filter items list is empty')

            sql = text(
                'SELECT * FROM product WHERE filters @> ARRAY[{}];'.format(
                    str(conditions).replace('[', '').replace(']', '')
                )
            )
            _products = db_session.execute(sql)
            products = []
            for product in _products:
                products.append({
                    'id': product[0],
                    'name': product[1],
                    'slug_name': product[2],
                    'description': product[3],
                    'images': self._get_product_photos(product[0]),
                    'attributes': self._get_product_attributes(product[0])
                })

            result['products'] = products

            db_session.commit()

            _filters = db_session.query(
                Attribute,
                AttributeValue
            ).distinct(
                AttributeValue.id
            ).outerjoin(
                AttributeValue,
                Attribute.id == AttributeValue.attribute_id
            ).outerjoin(
                ProductAttributeValues,
                AttributeValue.id == ProductAttributeValues.attribute_value_id
            ).outerjoin(
                Product,
                Product.id == ProductAttributeValues.product_id
            ).filter(
                Product.id.in_([i['id'] for i in result['products']])
            ).all()

            for _filter in _filters:
                filters.add(_filter)

            result['filters'] = self._get_filters(filters)

            self.write(ujson.dumps(result))
        except (TypeError, ValueError) as e:
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
