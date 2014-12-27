# -*- coding: utf-8 -*-

from flask import Blueprint

from .home import HomeView, WelcomeView, AboutView, MembersRecommendView
from .user import (OAuthCodeView, LoginView, LogoutView,
                   ProfileView, MembersView, FollowerView,
                   FollowingView, FeedView)
from .media import TagView, MediaProfileView
from .search import SearchUserView, SearchTagView
from .show import RealtimeView, ShowView
from .sitemap import ShowSitemapView, LikeSitemapView, UserSitemapView

blueprint = Blueprint('view', __name__)

blueprint.add_url_rule('/',
                       view_func=HomeView.as_view(b'home'),
                       endpoint='home')
blueprint.add_url_rule('/login/',
                       view_func=LoginView.as_view(b'login'),
                       endpoint='login')
blueprint.add_url_rule('/logout/',
                       view_func=LogoutView.as_view(b'logout'),
                       endpoint='logout')
blueprint.add_url_rule('/instagram/redirect/',
                       view_func=OAuthCodeView.as_view(b'oauthcode'),
                       endpoint='oauthcode')
blueprint.add_url_rule('/profile/<ukey>/',
                       view_func=ProfileView.as_view(b'profile'),
                       endpoint='profile')
blueprint.add_url_rule('/members/',
                       view_func=MembersView.as_view(b'members'),
                       endpoint='members')
blueprint.add_url_rule('/members/recommend/',
                       view_func=MembersRecommendView.as_view(b'recommend'),
                       endpoint='recommend')
blueprint.add_url_rule('/search/user/',
                       view_func=SearchUserView.as_view(b'search_user'),
                       endpoint='search_user')
blueprint.add_url_rule('/search/tag/',
                       view_func=SearchTagView.as_view(b'search_tag'),
                       endpoint='search_tag')
blueprint.add_url_rule('/media/<mid>/',
                       view_func=MediaProfileView.as_view(b'media'),
                       endpoint='media')
blueprint.add_url_rule('/tag/<name>/',
                       view_func=TagView.as_view(b'tag'),
                       endpoint='tag')
blueprint.add_url_rule('/follower/<ukey>/',
                       view_func=FollowerView.as_view(b'follower'),
                       endpoint='follower')
blueprint.add_url_rule('/following/<ukey>/',
                       view_func=FollowingView.as_view(b'following'),
                       endpoint='following')
blueprint.add_url_rule('/welcome/',
                       view_func=WelcomeView.as_view(b'welcome'),
                       endpoint='welcome')
blueprint.add_url_rule('/show/',
                       view_func=ShowView.as_view(b'show'),
                       endpoint='show')
blueprint.add_url_rule('/show/time/',
                       view_func=ShowView.as_view(b'show_time'),
                       endpoint='show_time',
                       defaults={'time_order': True})
blueprint.add_url_rule('/about/',
                       view_func=AboutView.as_view(b'about'),
                       endpoint='about')
blueprint.add_url_rule('/instagram/realtime/',
                       view_func=RealtimeView.as_view(b'realtime'),
                       endpoint='realtime')
blueprint.add_url_rule('/feed/',
                       view_func=FeedView.as_view(b'feed'),
                       endpoint='feed')


blueprint.add_url_rule(
    '/user/sitemap.xml', endpoint='user_sitemap',
    view_func=UserSitemapView.as_view(b'user_sitemap'))
blueprint.add_url_rule(
    '/like/sitemap.xml', endpoint='like_sitemap',
    view_func=LikeSitemapView.as_view(b'like_sitemap'))
blueprint.add_url_rule(
    '/show/sitemap.xml', endpoint='show_media',
    view_func=ShowSitemapView.as_view(b'show_sitemap'))
