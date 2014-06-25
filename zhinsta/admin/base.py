# -*-coding: utf-8 -*-
#!/usr/bin/env python
from __future__ import unicode_literals

"""
File:   base.py
Author: goodspeed
Email:  cacique1103@gmail.com
Github: https://github.com/zongxiao
Date:   <`3:2014-06-23`>
Description: admin base
"""

from flask import session, redirect, url_for
from flask.ext.admin import AdminIndexView, expose
from flask.ext.admin.contrib import sqla
from flask.ext.admin.form import rules

from zhinsta.engines import db
from zhinsta.models.user import AdminModel


def is_admin():
    ukey = session.get('ukey', '')
    if not ukey:
        return False
    return True if session.get('is_admin', False) else False


class ZhinstaAdminIndexView(AdminIndexView):

    @expose('/')
    def index(self):
        admin = is_admin()
        if not admin:
            return redirect(url_for('view.show'))
        return super(ZhinstaAdminIndexView, self).index()


class BaseAdmin(sqla.ModelView):

    def is_accessible(self):
        return is_admin()

    def is_text_column_type(self, name):
        if name:
            name = name.lower()
        return name in ('string', 'unicode', 'text', 'unicodetext', 'varchar')


class ZhinstaAdmin(BaseAdmin):
    '''zhinsta 管理员管理'''

    column_list = ('ukey', 'date_created')

    form_columns = ['ukey']

    def __init__(self, **kwargs):
        super(ZhinstaAdmin, self).__init__(AdminModel, db.session, **kwargs)
