# -*-coding: utf-8 -*-
from __future__ import unicode_literals

"""
File:   similar_user.py
Author: goodspeed
Email:  cacique1103@gmail.com
Github: https://github.com/zongxiao
Date:   3:2014-09-22
Description: 关注他的人也关注

followed_by 关注我的人/关注者 followed_by
follows     关注的人          follows

"""


from flask import request, views

import gevent

import instagram
from instagram import InstagramAPI

from zhinsta.app import app
from zhinsta.utils import spawn
from zhinsta.utils import render
from zhinsta.utils import is_admin
from zhinsta.utils import notfound
from zhinsta.utils import get_errors
from zhinsta.utils import open_visit
from zhinsta.utils import error_handle
from zhinsta.utils import login_required


class SimilarUserBase(object):

    def _get_users(self, ukey, token, next_url=None, user_type='followed_by'):
        # 每次取50
        api = InstagramAPI(access_token=token)
        if user_type == 'follows':
            # 关注的人
            users = spawn(api.user_follows, ukey, with_next_url=next_url)
        elif user_type == 'followed_by':
            # 关注我的人
            users = spawn(api.user_followed_by, ukey, with_next_url=next_url)

        gevent.joinall([users])
        users = users.get()
        errors = get_errors(users)
        if errors:
            app.logger.error(str(e) for e in errors)
            return [], None

        next_url = users[1]
        users = users[0]
        return users, next_url

    def _get_limit_users(self, ukey, token, limit, user_type):
        limit_users = []
        url = None
        for i in xrange((limit + 49) / 50):
            if i > 0 and not url:
                break
            users, url = self._get_users(
                ukey, token, next_url=url, user_type=user_type)
            if not users:
                break
            limit_users.extend(users)
        return limit_users[:limit]

    def _get_similar_users(self, ukey, all_follows, limit=12):
        follows_dict = {}
        for user in all_follows:
            if not isinstance(user, instagram.models.User):
                continue
            users = follows_dict.get(user.id, [])
            users.append(user)
            follows_dict[user.id] = users
        follows_dict_sort = sorted(
            follows_dict, key=lambda k: len(follows_dict[k]), reverse=True)
        similars = [follows_dict[id][0] for id in follows_dict_sort
                    if id != ukey]
        return similars[:limit]


class SimilarUserView(views.MethodView, SimilarUserBase):

    @error_handle
    @open_visit
    @login_required
    def get(self, ukey):
        admin = is_admin()
        if not admin:
            return notfound(u'页面不存在')
        x = int(request.args.get('x', 200))
        y = int(request.args.get('y', 100))
        is_fast = request.args.get('is_fast', False)
        # 获取关注者列表
        token = request.access_token
        followed_by = self._get_limit_users(ukey, token, x, 'followed_by')
        # 关注我的人关注的人
        all_follows = []
        if is_fast:
            # 使用gevent 提高速度 貌似有问题数量多了会报错
            user_follows = []
            for user in followed_by:
                user_follow = spawn(self._get_limit_users,
                                    user.id, token, y, 'follows')
                user_follows.append(user_follow)
            gevent.joinall(user_follows)
            for follows in user_follows:
                all_follows.extend(follows.get())
        else:
            for user in followed_by:
                user_follow = self._get_limit_users(user.id, token, y, 'follows')
                if isinstance(user_follow, list):
                    all_follows.extend(user_follow)
        similars = self._get_similar_users(ukey, all_follows)

        context = {'similars': similars[:12]}
        return render('similar.html', **context)


class RecommendUserView(views.MethodView, SimilarUserBase):

    @error_handle
    @open_visit
    @login_required
    def get(self, ukey):
        admin = is_admin()
        if not admin:
            return notfound(u'页面不存在')
        x = int(request.args.get('x', 200))
        y = int(request.args.get('y', 100))
        is_fast = request.args.get('is_fast', False)
        ukey = ukey or request.ukey
        # 获取我关注的人列表
        token = request.access_token
        followings = self._get_limit_users(ukey, token, x, 'follows')
        # 关注我的人关注的人
        all_follows = []
        if is_fast:
            # 使用gevent 提高速度 貌似有问题数量多了会报错
            user_follows = []
            for user in followings:
                user_follow = spawn(self._get_limit_users,
                                    user.id, token, y, 'follows')
                user_follows.append(user_follow)
            gevent.joinall(user_follows)
            for follows in user_follows:
                all_follows.extend(follows.get())
        else:
            for user in followings:
                user_follow = self._get_limit_users(user.id, token, y, 'follows')
                if isinstance(user_follow, list):
                    all_follows.extend(user_follow)
        similars = self._get_similar_users(ukey, all_follows)

        context = {'similars': similars[:12]}
        return render('similar.html', **context)
