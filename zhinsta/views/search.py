# -*- coding: utf-8 -*-

import gevent

from flask import views
from flask import request
from instagram import InstagramAPI
from instagram import InstagramAPIError

from zhinsta.utils import error_handle
from zhinsta.utils import login_required
from zhinsta.utils import notfound
from zhinsta.utils import open_visit
from zhinsta.utils import render

members_per_page = 48


class SearchUserView(views.MethodView):

    @error_handle
    @open_visit
    @login_required
    def get(self):
        wd = request.args.get('wd', '')
        api = InstagramAPI(access_token=request.access_token)
        users = gevent.spawn(api.user_search, wd)
        gevent.joinall([users])
        try:
            users = users.get()
        except InstagramAPIError, e:
            if e.error_type == 'APINotAllowedError':
                return render('search-user.html', wd=wd)
            return notfound(u'服务器暂时出问题了')
        return render('search-user.html', users=users, wd=wd)


class SearchTagView(views.MethodView):

    @error_handle
    @open_visit
    @login_required
    def get(self):
        wd = request.args.get('wd', '')
        api = InstagramAPI(access_token=request.access_token)
        tags = gevent.spawn(api.tag_search, wd)
        gevent.joinall([tags])
        try:
            tags = tags.get()
        except InstagramAPIError, e:
            if e.error_type == 'APINotAllowedError':
                return render('search-tag.html', wd=wd)
            return notfound(u'服务器暂时出问题了')
        return render('search-tag.html', tags=tags[0], wd=wd)
