# -*-coding: utf-8 -*-
#!/usr/bin/env python
from __future__ import unicode_literals

"""
File:   user.py
Author: goodspeed
Email:  cacique1103@gmail.com
Github: https://github.com/zongxiao
Date:   <`3:2014-06-23`>
Description: user manage
"""

from flask import url_for
from jinja2 import Markup

from base import BaseAdmin

from zhinsta.engines import db
from zhinsta.models.user import ShowModel


class ShowAdmin(BaseAdmin):

    column_list = ('mid', 'pic', 'ukey', 'user_pic', 'username',
                   'date_created', 'showable', 'hour_tagged')
    column_searchable_list = ('username', 'ukey')
    form_columns = ['mid', 'pic', 'ukey', 'user_pic', 'username',
                    'date_created', 'showable', 'hour_tagged']

    def _show_pic(self, context, model, name):
        return Markup('<img src=%s width=200 height=200>' % model.pic)

    def _show_user(self, context, model, name):
        return Markup('<a href="%s">%s</a>' % (
            url_for('view.profile', ukey=model.ukey),
            model.username))

    def _show_user_pic(self, context, model, name):
        return Markup('<a href="%s"><img src=%s width=90 height=90></a>' % (
            url_for('view.profile', ukey=model.ukey),
            model.user_pic))

    column_formatters = {
        'username': _show_user,
        'user_pic': _show_user_pic,
        'pic': _show_pic,
    }

    def __init__(self, **kwargs):
        super(ShowAdmin, self).__init__(ShowModel, db.session, **kwargs)
