__author__ = 'markel'

import tornado

from tornado.options import options
import tornado.web
import tornado.httpserver
import tornado.ioloop
from options import load_options
from handlers import *

load_options()

handlers = [
	(options.api_version, MainHandler),
	('{}/{}'.format(options.api_version, 'product/(?P<id>[^\/]+)'), ProductHandler),
	('{}/{}'.format(options.api_version, 'products'), ProductsHandler)
]

print(handlers)
print(options.as_dict())

if __name__ == "__main__":

	tornado_app = tornado.web.Application(handlers)
	server = tornado.httpserver.HTTPServer(tornado_app)
	server.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()
