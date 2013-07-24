# -*- coding: utf-8 -*-

import uuid

from flask import views
from flask import request
from flask import redirect
from flask import url_for
from flask import session
from flask import render_template

from ..instagram.client import InstagramAPI

from ..settings import INSTAGRAM_CLIENT_ID
from ..settings import INSTAGRAM_CLIENT_SECRET
from ..settings import INSTAGRAM_REDIRECT_URI
from ..settings import INSTAGRAM_SCOPE
from ..models.user import UserModel
from .utils import login_required
from ..engines import db


class HomeView(views.MethodView):

    def get(self):
        return render_template('login.html')


class ProfileView(views.MethodView):

    @login_required
    def get(self):
        api = InstagramAPI(access_token=request.access_token)
        return api.user().username


class OAuthCodeView(views.MethodView):

    def get(self):
        code = request.args.get('code', '')
        api = InstagramAPI(client_id=INSTAGRAM_CLIENT_ID,
                       client_secret=INSTAGRAM_CLIENT_SECRET,
                       redirect_uri=INSTAGRAM_REDIRECT_URI)
        access_token = api.exchange_code_for_access_token(code)
        user = (UserModel.query
                .filter_by(username=access_token[1]['username']).first())
        if user:
            user.access_token = access_token[0]
        else:
            user = UserModel(ukey=uuid.uuid4().hex,
                             username=access_token[1]['username'],
                             access_token=access_token[0])
            db.session.add(user)
        db.session.commit()
        session['ukey'] = user.ukey
        session['access_token'] = user.access_token
        return 'ok'


class LoginView(views.MethodView):

    def get(self):
        api = InstagramAPI(client_id=INSTAGRAM_CLIENT_ID,
                           client_secret=INSTAGRAM_CLIENT_SECRET,
                           redirect_uri=INSTAGRAM_REDIRECT_URI)
        redirect_uri = api.get_authorize_login_url(scope=INSTAGRAM_SCOPE)
        return redirect(redirect_uri)


class LogoutView(views.MethodView):

    @login_required
    def get(self):
        session.pop('ukey', None)
        session.pop('access_token', None)
        return redirect(url_for('view.home'))
