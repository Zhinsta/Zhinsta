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

import gevent

from instagram import InstagramAPI
from instagram import InstagramAPIError

from flask import session, redirect, url_for, request
from flask.ext.admin import AdminIndexView, expose
from flask.ext.admin.contrib import sqla

from zhinsta.engines import db
from zhinsta.utils import notfound
from zhinsta.models.user import AdminModel, RecommendModel


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

    def _get_user_avatar(self, users, api):
        users_list = []
        users_dict = {}
        for user in users:
            user = gevent.spawn(api.user, user_id=user.ukey)
            users_list.append(user)

        try:
            gevent.joinall(users_list)
        except InstagramAPIError:
            return notfound(u'服务器暂时出问题了')
        for user in users_list:
            user = user.value
            if user:
                users_dict[user.id] = user.profile_picture
        return users_dict

    @expose('/update_recommend_avatar')
    def update_avatar_view(self):
        total = RecommendModel.query.count()
        limit = 50
        offset = 0
        access_token = session.get('access_token', '')
        api = InstagramAPI(access_token=access_token)
        for i in xrange(offset, total, limit):
            users = (RecommendModel.query
                     .order_by(RecommendModel.order.desc())
                     .offset(offset)
                     .limit(limit)
                     .all())
            users_dict = self._get_user_avatar(users, api)
            for user in users:
                avatar = users_dict.get(user.ukey, '')
                if avatar and user.pic != avatar:
                    user.pic = avatar
            offset += limit
            db.session.commit()
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
