# -*- coding: utf-8 -*-

from functools import wraps

from flask import session
from flask import request
from flask import redirect
from flask import url_for

from ..models.user import UserModel


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not session.get('ukey', '') or not session.get('access_token', ''):
            #return redirect(url_for('view.login'))
            return 'not login'
        user = UserModel.query.get(session['ukey'])
        if not user:
            #return redirect(url_for('view.login'))
            return 'not login'
        request.ukey = session['ukey']
        request.access_token = session['access_token']
        return func(*args, **kwargs)
    return wrapper
