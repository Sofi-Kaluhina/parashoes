# coding: utf-8
__author__ = 'markel'

import os

import tornado.options
from tornado import template

from tornado.options import define
from unipath import Path


#: A place to look for config.
CONFIG_PATH = Path('/etc/bulavka/bulavka.conf')


def safe_define(*args, **kwargs):
    try:
        define(*args, **kwargs)
    except:
        pass

def define_options():
    # Generics ----------------------------------------------------------------
    safe_define(
        'api_version',
        default='/api/v1',
        help='API version',
        type=str,
    )
    safe_define(
        'debug',
        default=False,
        help='Run in debug mode',
        type=bool,
    )
    safe_define(
        'logging',
        default='debug',
        help='Logging level',
        type=str,
    )
    safe_define(
        'public_host',
        default='bulavka',
        help='Public host',
        type=str,
    )
    define(
        'port',
        default=8000,
        type=int,
        help='Run on the given port',
    )
    define(
        'template_loader',
        default=template.Loader(os.path.dirname(__file__)),
        help='Template loader'
    )
    define(
        'static_dir',
        default='/opt/apps/spa_request_handler/static',
        type=str,
        help='Static directory',
    )
    define(
        'media_dir',
        default='/opt/apps/spa_request_handler/media',
        type=str,
        help='Media directory',
    )
    # Database ----------------------------------------------------------------
    safe_define(
        'db_url',
        default='postgresql://postgres:postgres@localhost:5432/bulavka',
        help='DataBase DB URL',
        type=str,
    )

def load_options():
    define_options()
    if CONFIG_PATH.exists():
        tornado.options.parse_config_file(CONFIG_PATH, final=False)

    return tornado.options.parse_command_line()
