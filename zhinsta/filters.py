# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import random
import base64
from urlparse import urlparse
from datetime import datetime
from datetime import timedelta

import pyDes

from .app import app


URL_CRYPT_KEY = os.environ['ZHINSTA_CRYPT_KEY']


@app.template_filter()
def timestamp(value):
    if not isinstance(value, (int, long, float)):
        value = 0
    return datetime.fromtimestamp(value)


@app.template_filter()
def parseisoformat(value):
    return datetime.parseisoformat(value)


@app.template_filter()
def iproxy(url):
    if isinstance(url, unicode):
        url = url.encode('utf-8')
    url = urlparse(url)
    src = url.netloc + url.path
    cipher = pyDes.des(URL_CRYPT_KEY, padmode=pyDes.PAD_PKCS5)
    dst = cipher.encrypt(src, padmode=pyDes.PAD_PKCS5)
    return 'http://img{}.zhinsta.com:8000/{}'.format(random.choice([1, 2]), base64.urlsafe_b64encode(dst).strip())


@app.template_filter()
def time_since(dt, default='刚刚'):
    """将 datetime 替换成字符串 ('3小时前', '2天前' 等等)
    的 Jinja filter copy from
    https://github.com/tonyblundell/socialdump/blob/master/socialdump.py
    """
    if not dt:
        return ''

    now = datetime.now()
    diff = now - dt
    diff = diff - timedelta(seconds=28800)
    total_seconds = int(diff.total_seconds())
    if total_seconds > 0:
        if total_seconds < 315360000:
            periods = (
                (total_seconds / 86400, '天'),
                (total_seconds / 3600, '小时'),
                (total_seconds / 60, '分钟'),
                (total_seconds, '秒'),
            )
            for period, unit in periods:
                if period > 0:
                    return '%d%s前' % (period, unit)
            return default
        elif total_seconds < 86400 and dt.day == now.day:
            return '今天 ' + dt.strftime('%H:%M')
        else:
            return unicode(dt.strftime('%Y-%m-%d %H:%M'))
    else:
        return default
