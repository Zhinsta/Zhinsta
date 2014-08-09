# -*- coding: utf-8 -*-

import gevent
import random
from gevent.util import wrap_errors

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
from zhinsta.models.user import LikeModel
from zhinsta.models.user import AdminModel
from zhinsta.models.user import ShowModel
from zhinsta.settings import OPEN_ACCESS_TOKENS
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
        media = gevent.spawn(wrap_errors(InstagramAPIError, api.media), likes[0].media)
        gevent.joinall([media])
        media = media.get()
        if isinstance(media, InstagramAPIError):
            return notfound(u'服务器暂时出问题了')
        medias = ShowModel.query.filter(ShowModel.mid.in_([x.media for x in likes]))
        users = (RecommendModel.query
                 .order_by(RecommendModel.order.desc())
                 .limit(24).all())
        return render('login.html',
                      media=media,
                      medias=medias,
                      users=users)


class ProfileView(views.MethodView):

    @error_handle
    @open_visit
    @login_required
    def get(self, ukey):
        next_url = request.args.get('next_url', None)
        api = InstagramAPI(access_token=request.access_token)

        user = gevent.spawn(wrap_errors(InstagramAPIError, api.user), user_id=ukey)
        feeds = gevent.spawn(wrap_errors(InstagramAPIError, api.user_recent_media),
                             user_id=ukey, with_next_url=next_url)
        if request.ukey:
            isfollows = gevent.spawn(isfollow, ukey, api)
        else:
            isfollows = gevent.spawn(lambda x: False, ukey)

        gevent.joinall([user, feeds, isfollows])
        user, feeds, isfollows = user.get(), feeds.get(), isfollows.get()
        errors = [e for e in (user, feeds, isfollows) if isinstance(e, InstagramAPIError)]
        if errors:
            if any([e.error_type == 'APINotAllowedError' for e in errors]):
                return render('profile-noauth.html', ukey=ukey)
            return notfound(u'服务器暂时出问题了')

        next_url = feeds[1] if feeds else None
        feeds = feeds[0] if feeds else []
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
        admin = AdminModel.query.get(user.ukey)
        session.permanent = True
        session['ukey'] = user.ukey
        session['username'] = user.username
        session['access_token'] = user.access_token
        session['is_admin'] = True if admin else False
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
        redirect_uri = gevent.spawn(api.get_authorize_login_url,
                                    scope=INSTAGRAM_SCOPE)
        gevent.joinall([redirect_uri])
        try:
            redirect_uri = redirect_uri.get()
        except InstagramAPIError:
            return notfound(u'服务器暂时出问题了')
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


class MediaProfileView(views.MethodView):

    @error_handle
    @open_visit
    @login_required
    def get(self, mid):
        api = InstagramAPI(access_token=request.access_token)
        media = gevent.spawn(api.media, mid)
        likes = gevent.spawn(api.media_likes, media_id=mid)
        gevent.joinall([media, likes])
        try:
            media, likes = media.get(), likes.get()
        except InstagramAPIError:
            return notfound(u'服务器暂时出问题了')

        ukey = media.user.id
        isfollows = False
        if request.ukey:
            isfollows = gevent.spawn(isfollow, ukey, api)
        else:
            isfollows = gevent.spawn(lambda x: False, ukey)

        gevent.joinall([isfollows])
        try:
            isfollows = isfollows.get()
        except InstagramAPIError:
            return notfound(u'服务器暂时出问题了')

        isstar = False
        for i in likes:
            if request.ukey and request.ukey == i.id:
                isstar = True

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
        next_url = request.args.get('next_url', None)

        api = InstagramAPI(access_token=request.access_token)
        tag = api.tag(name)
        media = api.tag_recent_media(tag_name=name,
                                     with_next_url=next_url)
        tag = gevent.spawn(api.tag, name)
        media = gevent.spawn(api.tag_recent_media,
                             tag_name=name, with_next_url=next_url)
        gevent.joinall([tag, media])
        try:
            tag, media = tag.get(), media.get()
        except InstagramAPIError:
            return notfound(u'服务器暂时出问题了')

        next_url = media[1]
        media = media[0]
        return render('tag.html', tag=tag, media=media, next_url=next_url)


class FollowBaseView(object):

    def _get_users(self, ukey, user_type='followed'):
        next_url = request.args.get('next_url', None)
        api = InstagramAPI(access_token=request.access_token)
        user = gevent.spawn(api.user, ukey)
        if user_type == 'following':
            users = gevent.spawn(api.user_follows,
                                 ukey, with_next_url=next_url)
        else:
            users = gevent.spawn(api.user_followed_by,
                                 ukey, with_next_url=next_url)
        isfollows = False
        if request.ukey:
            isfollows = gevent.spawn(isfollow, ukey, api)
        else:
            isfollows = gevent.spawn(lambda x: False, ukey)

        gevent.joinall([user, users, isfollows])
        try:
            user, users, isfollows = user.get(), users.get(), isfollows.get()
        except InstagramAPIError:
            return notfound(u'服务器暂时出问题了')

        next_url = users[1]
        users = users[0]

        isme = False
        if request.ukey and ukey == request.ukey:
            isme = True
        context = {
            'user': user,
            'users': users,
            'next_url': next_url,
            'isfollows': isfollows,
            'isme': isme,
        }
        return context


class FollowerView(views.MethodView, FollowBaseView):

    @error_handle
    @open_visit
    @login_required
    def get(self, ukey):
        context = self._get_users(ukey)
        if isinstance(context, tuple):
            return context
        context['message'] = u'关注者'
        return render('follower.html', **context)


class FollowingView(views.MethodView, FollowBaseView):

    @error_handle
    @open_visit
    @login_required
    def get(self, ukey):
        context = self._get_users(ukey, user_type='following')
        if isinstance(context, tuple):
            return context
        context['message'] = u'关注中'
        return render('follower.html', **context)


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
        next_url = request.args.get('next_url', None)

        api = InstagramAPI(access_token=request.access_token)
        feed = gevent.spawn(api.user_media_feed, with_next_url=next_url)

        gevent.joinall([feed])
        try:
            feed = feed.get()
        except InstagramAPIError:
            return notfound(u'服务器暂时出问题了')

        next_url = feed[1]
        media = feed[0]
        return render('feed.html', media=media, next_url=next_url)
