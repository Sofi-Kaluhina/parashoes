__author__ = 'markel'

import os
import sys

sys.path.append(os.path.dirname(__file__))

from tornado.options import options
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.web import FallbackHandler, Application

from admin.admin import app
from handlers import *

tr = WSGIContainer(app)

handlers = [
    ('{}/{}'.format(options.api_version, 'categories'), CategoriesHandler),
    ('{}/{}'.format(options.api_version, 'product/(?P<slug_name>[^\/]+)'), ProductHandler),
    ('{}/{}'.format(options.api_version, 'products'), ProductsHandler),
    ('{}/{}'.format(options.api_version, 'init'), InitHandler),
    ('.*', FallbackHandler, dict(fallback=tr))
]

if __name__ == "__main__":
    tornado_app = Application(handlers, debug=True)
    server = HTTPServer(tornado_app)
    server.listen(options.port)
    IOLoop.instance().start()
