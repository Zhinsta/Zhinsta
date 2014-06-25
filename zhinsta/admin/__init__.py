# -*-coding: utf-8 -*-
from __future__ import unicode_literals

from flask.ext.admin import Admin

from user import UserAdmin
from show import ShowAdmin
from like import LikeAdmin
from recommend import RecommendAdmin
from base import ZhinstaAdminIndexView, ZhinstaAdmin

zhinsta_admin = Admin(name='Zhinsta后台管理',
                      index_view=ZhinstaAdminIndexView(),
                      url='/admin')

zhinsta_admin.add_view(UserAdmin(name='用户列表'))
zhinsta_admin.add_view(LikeAdmin(name='喜欢列表'))
zhinsta_admin.add_view(ShowAdmin(name='展台列表'))
zhinsta_admin.add_view(RecommendAdmin(name='推荐列表'))
zhinsta_admin.add_view(ZhinstaAdmin(name='管理员列表'))
