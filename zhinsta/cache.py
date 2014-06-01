# coding: utf-8

from flask.ext.cache import Cache

from zhinsta.app import app

cache = Cache(app, config={'CACHE_TYPE': 'redis'})
