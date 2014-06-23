# -*- coding: utf-8 -*-

import gevent

from flask import views
from flask import request
from flask import redirect
from flask import url_for
from flask import session

from instagram import InstagramAPI
from instagram import InstagramAPIError

from zhinsta.engines import db
from zhinsta.models.user import RecommendModel
from zhinsta.models.user import UserModel
from zhinsta.settings import INSTAGRAM_CLIENT_ID
from zhinsta.settings import INSTAGRAM_CLIENT_SECRET
from zhinsta.settings import INSTAGRAM_REDIRECT_URI
from zhinsta.settings import INSTAGRAM_SCOPE
from zhinsta.utils import Pager
from zhinsta.utils import apierror
from zhinsta.utils import error_handle
from zhinsta.utils import has_login
from zhinsta.utils import isfollow
from zhinsta.utils import login_required
from zhinsta.utils import notfound
from zhinsta.utils import open_visit
from zhinsta.utils import render

members_per_page = 20


class HomeView(views.MethodView):

    @error_handle
    def get(self):
        if has_login():
            return redirect(url_for('view.show'))
        return render('login.html')


class ProfileView(views.MethodView):

    @error_handle
    @open_visit
    @login_required
    def get(self, ukey):
        next_url = request.args.get('next_url', None)
        api = InstagramAPI(access_token=request.access_token)

        user = gevent.spawn(api.user, user_id=ukey)
        feeds = gevent.spawn(api.user_recent_media, user_id=ukey, with_next_url=next_url)
        if request.ukey:
            isfollows = gevent.spawn(isfollow, ukey, api)
        else:
            isfollows = gevent.spawn(lambda x: False, ukey)

        try:
            gevent.joinall([user, feeds, isfollows])
        except InstagramAPIError, e:
            if e.error_type == 'APINotAllowedError':
                return render('profile-noauth.html', ukey=ukey)
            return notfound(u'服务器暂时出问题了')
        user, feeds, isfollows = user.value, feeds.value, isfollows.value

        next_url = feeds[1]
        feeds = feeds[0]
        isme = False
        if request.ukey and ukey == request.ukey:
            isme = True
        return render(
            'profile.html',
            user=user,
            feeds=feeds,
            isme=isme,
            isfollow=isfollows,
            next_url=next_url
        )


class OAuthCodeView(views.MethodView):

    @error_handle
    def get(self):
        if has_login():
            return redirect(url_for('view.show'))
        redirect_url = url_for('view.show')
        code = request.args.get('code', '')
        redirect_uri = INSTAGRAM_REDIRECT_URI
        if request.args.get('uri', ''):
            redirect_url = request.args.get('uri')
            redirect_uri += '?uri=' + redirect_url
        api = InstagramAPI(client_id=INSTAGRAM_CLIENT_ID,
                           client_secret=INSTAGRAM_CLIENT_SECRET,
                           redirect_uri=redirect_uri)
        try:
            access_token = api.exchange_code_for_access_token(code)
        except:
            return apierror()
        user = (UserModel.query
                .filter_by(ukey=access_token[1]['id']).first())
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
            redirect_url = url_for('view.welcome')
        db.session.commit()
        session.permanent = True
        session['ukey'] = user.ukey
        session['username'] = user.username
        session['access_token'] = user.access_token
        return redirect(redirect_url)


class LoginView(views.MethodView):

    @error_handle
    def get(self):
        if has_login():
            return redirect(url_for('view.members'))
        redirect_uri = INSTAGRAM_REDIRECT_URI
        if request.args.get('uri', ''):
            redirect_uri += '?uri=' + request.args.get('uri')
        api = InstagramAPI(client_id=INSTAGRAM_CLIENT_ID,
                           client_secret=INSTAGRAM_CLIENT_SECRET,
                           redirect_uri=redirect_uri)
        redirect_uri = api.get_authorize_login_url(scope=INSTAGRAM_SCOPE)
        return redirect(redirect_uri)


class LogoutView(views.MethodView):

    @error_handle
    @login_required
    def get(self):
        session.pop('ukey', None)
        session.pop('username', None)
        session.pop('access_token', None)
        url = url_for('view.home')
        if request.args.get('uri', ''):
            url = request.args.get('uri')
        return redirect(url)


class MembersView(views.MethodView):

    @error_handle
    def get(self):
        total = UserModel.query.count()
        current_page = request.args.get('page', 1)
        pager = Pager(members_per_page, total)
        pager.set_current_page(current_page)
        users = (UserModel.query
                 .order_by(UserModel.date_created.desc())
                 .offset(pager.offset)
                 .limit(pager.limit).all())
        return render('members.html', users=users, pager=pager)


class SearchUserView(views.MethodView):

    @error_handle
    @open_visit
    @login_required
    def get(self):
        wd = request.args.get('wd', '')
        api = InstagramAPI(access_token=request.access_token)
        users = api.user_search(wd)
        return render('search-user.html', users=users, wd=wd)


class SearchTagView(views.MethodView):

    @error_handle
    @open_visit
    @login_required
    def get(self):
        wd = request.args.get('wd', '')
        api = InstagramAPI(access_token=request.access_token)
        tags = api.tag_search(wd)[0]
        return render('search-tag.html', tags=tags, wd=wd)


class MediaProfileView(views.MethodView):

    @error_handle
    @open_visit
    @login_required
    def get(self, mid):
        api = InstagramAPI(access_token=request.access_token)
        media = api.media(mid)
        likes = api.media_likes(media_id=mid)
        isstar = False
        for i in likes:
            if request.ukey and request.ukey == i.id:
                isstar = True
        ukey = media.user.id
        isfollows = False
        if request.ukey:
            isfollows = isfollow(ukey)
        isme = False
        if request.ukey and ukey == request.ukey:
            isme = True
        return render('media.html', media=media, isme=isme,
                      isfollow=isfollows, likes=likes[:5], isstar=isstar)


class TagView(views.MethodView):

    @error_handle
    @open_visit
    @login_required
    def get(self, name):
        api = InstagramAPI(access_token=request.access_token)
        tag = api.tag(name)
        next_url = request.args.get('next_url', None)
        media = api.tag_recent_media(tag_name=name,
                                     with_next_url=next_url)
        next_url = media[1]
        media = media[0]
        return render('tag.html', tag=tag, media=media, next_url=next_url)


class FollowerView(views.MethodView):

    @error_handle
    @open_visit
    @login_required
    def get(self, ukey):
        api = InstagramAPI(access_token=request.access_token)
        user = api.user(ukey)
        next_url = request.args.get('next_url', None)
        users = api.user_followed_by(ukey, with_next_url=next_url)
        next_url = users[1]
        users = users[0]
        isfollows = False
        if request.ukey:
            isfollows = isfollow(ukey)
        isme = False
        if request.ukey and ukey == request.ukey:
            isme = True
        return render('follower.html', user=user, users=users,
                      message=u'关注者', isme=isme, isfollow=isfollows,
                      next_url=next_url)


class FollowingView(views.MethodView):

    @error_handle
    @open_visit
    @login_required
    def get(self, ukey):
        api = InstagramAPI(access_token=request.access_token)
        user = api.user(ukey)
        next_url = request.args.get('next_url', None)
        users = api.user_follows(ukey, with_next_url=next_url)
        next_url = users[1]
        users = users[0]
        isfollows = False
        if request.ukey:
            isfollows = isfollow(ukey)
        isme = False
        if request.ukey and ukey == request.ukey:
            isme = True
        return render('follower.html', user=user, users=users,
                      message=u'关注中', isme=isme, isfollow=isfollows,
                      next_url=next_url)


class WelcomeView(views.MethodView):

    @error_handle
    @login_required
    def get(self):
        ukey = session.get('ukey', '')
        user = UserModel.query.get(ukey)
        return render('welcome.html', name=user.username, img=user.pic)


class ShowView(views.MethodView):

    @error_handle
    def get(self):
        return render('show.html')


class AboutView(views.MethodView):

    @error_handle
    def get(self):
        return render('about.html')


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


class FeedView(views.MethodView):

    @error_handle
    @login_required
    def get(self):
        api = InstagramAPI(access_token=request.access_token)
        next_url = request.args.get('next_url', None)
        feed = api.user_media_feed(with_next_url=next_url)
        next_url = feed[1]
        media = feed[0]
        return render('feed.html', media=media, next_url=next_url)
