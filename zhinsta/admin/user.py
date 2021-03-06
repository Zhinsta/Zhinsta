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

from jinja2 import Markup
from flask import url_for

from base import BaseAdmin
from zhinsta.engines import db
from zhinsta.models.user import UserModel


class UserAdmin(BaseAdmin):
    column_list = ('ukey', 'username', 'pic', 'date_created')
    column_searchable_list = ('username', 'ukey')
    column_filters = ('date_created',)

    def _show_pic(self, context, model, name):
        return Markup('<img src=%s width=90 height=90>' % model.pic)

    def _show_user(self, context, model, name):
        return Markup('<a href="%s">%s</a>' % (
            url_for('view.profile', ukey=model.ukey),
            model.username))

    column_formatters = {
        'username': _show_user,
        'pic': _show_pic,
    }

    def __init__(self, **kwargs):
        super(UserAdmin, self).__init__(UserModel, db.session, **kwargs)
