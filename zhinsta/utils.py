# -*- coding: utf-8 -*-

import json
import random
import time
import traceback
from functools import wraps

from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from instagram import InstagramAPI
from instagram import InstagramAPIError

from .engines import db
from .models.user import ShowModel
from .models.user import UserModel
from .settings import OPEN_ACCESS_TOKENS


def has_login():
    if not session.get('ukey', ''):
        return False
    if not session.get('access_token', ''):
        return False
    if not session.get('username', ''):
        return False
    user = UserModel.query.get(session['ukey'])
    if not user:
        return False
    return user


def open_visit(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        request.access_token = random.choice(OPEN_ACCESS_TOKENS)
        return func(*args, **kwargs)
    return wrapper


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not has_login():
            if not request.access_token:
                return redirect(url_for('view.login'))
        else:
            request.ukey = session['ukey']
            request.access_token = session['access_token']
        return func(*args, **kwargs)
    return wrapper


def render(template, **argkv):
    ukey = ''
    if request.ukey:
        ukey = request.ukey
    if ukey:
        argkv.update({'has_login': True,
                      'username': session.get('username', ''),
                      'ukey': ukey,
                      'request': request})
    else:
        argkv.update({'has_login': False})
    return render_template(template, **argkv)


def apierror(message=None, status_code=500):
    if not message:
        message = \
            u'服务器不给力，勇敢的少年啊，请重新试一次吧'
    return (render('error.html', message=message), status_code)


def notfound(message=u'404 not found', status_code=404):
    return apierror(message, status_code)


class Pager(object):

    def __init__(self, limit, total, url=None):
        self.limit = limit
        self.total = total
        self.total_page = (total - 1) / limit + 1
        self.current_page = 1
        self.offset = 0
        if not url:
            url = url_for(request.endpoint)
        if '?' in url:
            url = url + '&'
        else:
            if not url.endswith('/'):
                url = url + '/'
            url = url + '?'
        self.url = url + 'page='

    def set_offset(self, offset):
        offset = int(offset)
        if offset > self.total - 1:
            offset = self.total - 1
        if offset < 0:
            offset = 0
        self.offset = offset
        self.current_page = offset / self.limit + 1

    def set_current_page(self, current_page):
        current_page = int(current_page)
        if current_page > self.total_page:
            current_page = self.total_page
        if current_page < 1:
            current_page = 1
        self.current_page = current_page
        self.offset = (current_page - 1) * self.limit

    def __call__(self, length=5):
        start = 1
        if self.current_page > 2:
            start = self.current_page - 2
        end = start + length - 1
        if end > self.total_page:
            end = self.total_page
        pager = []
        for url in range(start, end + 1):
            active = False
            if url == self.current_page:
                active = True
            pager.append({'url': self.url + str(url),
                          'cnt': url,
                          'active': active})
        pre_url = self.url + str(start)
        if self.current_page > start:
            pre_url = self.url + str(self.current_page - 1)
        next_url = self.url + str(end)
        if self.current_page < self.total_page:
            next_url = self.url + str(self.current_page + 1)
        return render('pager.html', pager=pager,
                      pre_url=pre_url, next_url=next_url)


def error_handle(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        request.ukey = session.get('ukey', '')
        request.access_token = session.get('access_token', '')
        try:
            return func(*args, **kwargs)
        except InstagramAPIError, e:
            if e.error_type == 'APINotAllowedError':
                return render('profile-noauth.html', ukey=request.ukey)
            traceback.print_exc()
            print e.error_message
            return apierror()
        except Exception, e:
            traceback.print_exc()
            print e.message
            return apierror()
    return wrapper


def api_error_handle(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except InstagramAPIError, e:
            traceback.print_exc()
            print e.error_message
            raise e
        except Exception, e:
            traceback.print_exc()
            print e.message
            raise e
    return wrapper


def isfollow(ukey, api=None):
    if not api:
        api = InstagramAPI(access_token=session.get('access_token', ''))
    data = api.user_relationship(user_id=ukey)
    outgoing = data.outgoing_status
    if outgoing == 'follows':
        return True
    return False


def json_response(ret):
    return json.dumps({'result': ret})


def add_show(m):
    ret = False
    showm = ShowModel.query.get(m.id)
    if showm:
        ret = True
    else:
        hour = int(time.time() / 7200)
        showm = ShowModel(mid=m.id,
                          pic=m.images['low_resolution'].url,
                          user_pic=m.user.profile_picture,
                          ukey=m.user.id,
                          username=m.user.username,
                          date_created=m.created_time,
                          hour_tagged=hour)
        db.session.add(showm)
        db.session.commit()
    return ret
