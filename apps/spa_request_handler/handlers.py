__author__ = 'markel'

from tornado import web, gen, concurrent
from mock import get_random_products
import ujson


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


class ProductsHandler(CORSHandler):
	@gen.coroutine
	def get(self):
		future = get_random_products(0)
		try:
			self.write(ujson.dumps(concurrent.Future.result(future)))
		except gen.BadYieldError as e:
			self.write(e.args)


class ProductHandler(CORSHandler):
	def get(self, id):
		future = get_random_products(1)
		try:
			self.write(ujson.dumps(concurrent.Future.result(future)[int(id)]))
		except gen.BadYieldError as e:
			self.write(e.args)
