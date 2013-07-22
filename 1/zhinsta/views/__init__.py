# -*- coding: utf-8 -*-

from flask import Blueprint

from .home import (HomeView, OAuthCodeView, LoginView,
                   LogoutView, ProfileView)

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
blueprint.add_url_rule('/profile/',
                       view_func=ProfileView.as_view(b'profile'),
                       endpoint='profile')
