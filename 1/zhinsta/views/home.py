# -*- coding: utf-8 -*-

from flask import views
from flask import request
from flask import redirect
from flask import url_for
from flask import session

from ..instagram.client import InstagramAPI

from ..settings import INSTAGRAM_CLIENT_ID
from ..settings import INSTAGRAM_CLIENT_SECRET
from ..settings import INSTAGRAM_REDIRECT_URI
from ..settings import INSTAGRAM_SCOPE
from ..models.user import UserModel
from ..engines import db
from .utils import login_required
from .utils import has_login
from .utils import apierror
from .utils import error_handle
from .utils import notfound
from .utils import render
from .utils import Pager

members_per_page = 20


class HomeView(views.MethodView):

    @error_handle
    def get(self):
        if has_login():
            return redirect(url_for('view.members'))
        return render('login.html')


class ProfileView(views.MethodView):

    @error_handle
    @login_required
    def get(self, ukey):
        api = InstagramAPI(access_token=session.get('access_token', ''))
        try:
            user = api.user(user_id=ukey)
        except:
            return notfound(u'貌似这个用户你不能查看或者服务器暂时出问题了')
        feeds = api.user_recent_media(user_id=ukey)[0]
        return render('profile.html', user=user, feeds=feeds)


class OAuthCodeView(views.MethodView):

    @error_handle
    def get(self):
        if has_login():
            return redirect(url_for('view.members'))
        code = request.args.get('code', '')
        api = InstagramAPI(client_id=INSTAGRAM_CLIENT_ID,
                           client_secret=INSTAGRAM_CLIENT_SECRET,
                           redirect_uri=INSTAGRAM_REDIRECT_URI)
        try:
            access_token = api.exchange_code_for_access_token(code)
        except:
            return apierror()
        user = (UserModel.query
                .filter_by(ukey=access_token[1]['id']).first())
        redirect_url = 'view.members'
        if user:
            user.access_token = access_token[0]
            user.username = access_token[1]['username']
            user.pic = access_token[1]['profile_picture']
        else:
            user = UserModel(ukey=access_token[1]['id'],
                             username=access_token[1]['username'],
                             pic=access_token[1]['profile_picture'],
                             access_token=access_token[0])
            db.session.add(user)
            redirect_url = 'view.welcome'
        db.session.commit()
        session['ukey'] = user.ukey
        session['username'] = user.username
        session['access_token'] = user.access_token
        return redirect(url_for(redirect_url))


class LoginView(views.MethodView):

    @error_handle
    def get(self):
        if has_login():
            return redirect(url_for('view.members'))
        api = InstagramAPI(client_id=INSTAGRAM_CLIENT_ID,
                           client_secret=INSTAGRAM_CLIENT_SECRET,
                           redirect_uri=INSTAGRAM_REDIRECT_URI)
        redirect_uri = api.get_authorize_login_url(scope=INSTAGRAM_SCOPE)
        return redirect(redirect_uri)


class LogoutView(views.MethodView):

    @error_handle
    @login_required
    def get(self):
        session.pop('ukey', None)
        session.pop('username', None)
        session.pop('access_token', None)
        return redirect(url_for('view.home'))


class MembersView(views.MethodView):

    @error_handle
    @login_required
    def get(self):
        total = UserModel.query.count()
        current_page = request.args.get('page', 1)
        pager = Pager(members_per_page, total, url_for('view.members'))
        pager.set_current_page(current_page)
        users = (UserModel.query
                 .order_by(UserModel.date_created.desc())
                 .offset(pager.offset)
                 .limit(pager.limit).all())
        return render('members.html', users=users, pager=pager)


class SearchUserView(views.MethodView):

    @error_handle
    @login_required
    def get(self):
        wd = request.args.get('wd', '')
        api = InstagramAPI(access_token=session.get('access_token', ''))
        users = api.user_search(wd)
        return render('search-user.html', users=users, wd=wd)


class SearchTagView(views.MethodView):

    @error_handle
    @login_required
    def get(self):
        wd = request.args.get('wd', '')
        api = InstagramAPI(access_token=session.get('access_token', ''))
        tags = api.tag_search(wd)[0]
        return render('search-tag.html', tags=tags, wd=wd)


class MediaProfileView(views.MethodView):

    @error_handle
    @login_required
    def get(self, mid):
        api = InstagramAPI(access_token=session.get('access_token', ''))
        media = api.media(mid)
        return render('media.html', media=media)


class TagView(views.MethodView):

    @error_handle
    @login_required
    def get(self, name):
        api = InstagramAPI(access_token=session.get('access_token', ''))
        tag = api.tag(name)
        media = api.tag_recent_media(tag_name=name)[0]
        return render('tag.html', tag=tag, media=media)


class FollowerView(views.MethodView):

    @error_handle
    @login_required
    def get(self, ukey):
        api = InstagramAPI(access_token=session.get('access_token', ''))
        user = api.user(ukey)
        users = api.user_followed_by(ukey)[0]
        return render('follower.html', user=user, users=users)


class FollowingView(views.MethodView):

    @error_handle
    @login_required
    def get(self, ukey):
        api = InstagramAPI(access_token=session.get('access_token', ''))
        user = api.user(ukey)
        users = api.user_follows(ukey)[0]
        return render('follower.html', user=user, users=users)


class WelcomeView(views.MethodView):

    @error_handle
    @login_required
    def get(self):
        ukey = session.get('ukey', '')
        user = UserModel.query.get(ukey)
        return render('welcome.html', name=user.username, img=user.pic)
