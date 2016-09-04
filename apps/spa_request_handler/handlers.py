__author__ = 'markel'

from tornado import web, gen, concurrent
from mock import get_random_products
import ujson

from model import *
from connection import db_session


class MainHandler(web.RequestHandler):
    def get(self):
        self.write("Hello world")


class CORSHandler(web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Credentials", "true")
        self.set_header("Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS")
        self.set_header("Access-Control-Allow-Headers",
                        "Content-Type, Depth, User-Agent, X-File-Size, X-Requested-With, X-Requested-By, If-Modified-Since, X-File-Name, Cache-Control")


class HProducts(CORSHandler):
    def _get_product_attributes(self, product_id):
        query = db_session.query(
            Product,
            CatalogProductAttribute,
            ProductsProductAttribute
        ).filter(
            Product.id == product_id
        )
        query = query.join(
            ProductsProductAttribute,
            ProductsProductAttribute.product_id == Product.id
        )
        query = query.join(
            CatalogProductAttribute,
            CatalogProductAttribute.id == ProductsProductAttribute.catalog_product_attribute_id
        )
        result = {}
        attributes = query.all()
        for _, attribute_name, attribute_value in attributes:
            result[attribute_name.name] = attribute_value.attribute_value
        return result

    def _get_product_photos(self, product_id):
        query = db_session.query(
            Product,
            ProductPhoto,
            ProductsProductPhoto
        ).filter(
            Product.id == product_id
        )
        query = query.join(
            ProductsProductPhoto,
            Product.id == ProductsProductPhoto.product_id
        )
        query = query.join(
            ProductPhoto,
            ProductsProductPhoto.product_photo_id == ProductPhoto.id
        )

        photos = query.all()

        result = []
        for _, photo, _ in photos:
            result.append(
                {
                    'name': photo.name,
                    'path': 'media/product/{}'.format(photo.path),
                    'thumb_name': photo.thumb_name,
                    'thumb_path': 'media/product/thumb/{}'.format(photo.thumb_path),
                }
            )
        return result


class ProductsHandler(HProducts):
    @gen.coroutine
    def get(self):
        try:
            query = db_session.query(Product)
            products = query.all()

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

            self.write(ujson.dumps(result))
        except gen.BadYieldError as e:
            self.write(e.args)


class ProductHandler(HProducts):
    @gen.coroutine
    def get(self, id):
        try:
            query = db_session.query(Product).filter(Product.id == id)
            products = query.all()

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

            self.write(ujson.dumps(result))
        except gen.BadYieldError as e:
            self.write(e.args)

