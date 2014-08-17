# -*- coding: utf-8 -*-

import random

from flask import views
from flask import request
from flask import session
from instagram import InstagramAPI
from instagram import InstagramAPIError

from zhinsta.models.user import RecommendModel
from zhinsta.models.user import UserModel
from zhinsta.models.user import LikeModel
from zhinsta.models.user import ShowModel
from zhinsta.settings import OPEN_ACCESS_TOKENS
from zhinsta.utils import error_handle
from zhinsta.utils import login_required
from zhinsta.utils import notfound
from zhinsta.utils import render
from zhinsta.utils import Pager

members_per_page = 48


class HomeView(views.MethodView):

    @error_handle
    def get(self):
        likes = (LikeModel.query
                 .filter(LikeModel.ukey == '448621019')
                 .order_by(LikeModel.date_created.desc())
                 .limit(5).all())
        access_token = random.choice(OPEN_ACCESS_TOKENS)
        api = InstagramAPI(access_token=access_token)
        media = api.media(likes[0].media)
        if isinstance(media, InstagramAPIError):
            return notfound(u'服务器暂时出问题了')
        medias = ShowModel.query.filter(
            ShowModel.mid.in_([x.media for x in likes[1:]]))
        users = (RecommendModel.query
                 .order_by(RecommendModel.order.desc())
                 .limit(24).all())
        return render('home.html',
                      media=media,
                      medias=medias,
                      users=users)


class MembersRecommendView(views.MethodView):

    @error_handle
    def get(self):
        total = RecommendModel.query.count()
        current_page = request.args.get('page', 1)
        pager = Pager(members_per_page, total)
        pager.set_current_page(current_page)
        users = (RecommendModel.query
                 .order_by(RecommendModel.order.desc())
                 .offset(pager.offset)
                 .limit(pager.limit).all())
        return render('members.html', users=users, pager=pager)


class WelcomeView(views.MethodView):

    @error_handle
    @login_required
    def get(self):
        ukey = session.get('ukey', '')
        user = UserModel.query.get(ukey)
        return render('welcome.html', name=user.username, img=user.pic)


class AboutView(views.MethodView):

    @error_handle
    def get(self):
        return render('about.html')
