# -*- coding: utf-8 -*-

from flaskext.sqlalchemy import SQLAlchemy

from .app import app
from settings import (MYSQL_USER, MYSQL_PASS, MYSQL_HOST,
                      MYSQL_PORT, MYSQL_DB)

app.config['SQLALCHEMY_DATABASE_URI'] =\
    'mysql://%s:%s@%s:%s/%s?charset=utf8' %\
    (MYSQL_USER, MYSQL_PASS, MYSQL_HOST, MYSQL_PORT, MYSQL_DB)


class sae_SQLAlchemy(SQLAlchemy):

    def apply_driver_hacks(self, app, info, options):
        super(sae_SQLAlchemy, self).apply_driver_hacks(app, info, options)
        options['pool_recycle'] = 20


db = sae_SQLAlchemy(app)
