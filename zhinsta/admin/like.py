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
from zhinsta.models.user import LikeModel


class LikeAdmin(BaseAdmin):

    column_list = ('ukey', 'username', 'media',
                   'media_username', 'date_created')
    column_searchable_list = ('username', 'media_username', 'ukey')

    form_columns = ['ukey', 'username', 'media', 'media_username']

    def _show_media(self, context, model, name):
        return Markup('<img src=%s width=200 height=200>' % model.media)

    def _show_user(self, context, model, name):
        return Markup('<a href="%s">%s</a>' % (
            url_for('view.profile', ukey=model.ukey),
            model.username))

    column_formatters = {
        'username': _show_user,
        'media': _show_media,
    }

    def __init__(self, **kwargs):
        super(LikeAdmin, self).__init__(LikeModel, db.session, **kwargs)
