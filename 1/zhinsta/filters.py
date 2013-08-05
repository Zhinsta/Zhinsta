# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime
from datetime import timedelta

from .app import app


@app.template_filter()
def timestamp(value):
    if not isinstance(value, (int, long, float)):
        value = 0
    return datetime.fromtimestamp(value)


@app.template_filter()
def parseisoformat(value):
    return datetime.parseisoformat(value)


@app.template_filter()
def time_since(dt, default='刚刚'):
    """将 datetime 替换成字符串 ('3小时前', '2天前' 等等)
    的 Jinja filter copy from
    https://github.com/tonyblundell/socialdump/blob/master/socialdump.py
    sqlite 的 CURRENT_TIMESTAMP 只能使用 UTC 时间, 所以单元测试
    看到时间是8小时前的 don't panic, PostgreSQL 是有时区设定的.

    """
    # added by jade
    if not dt:
        return ''

    now = datetime.now()
    diff = now - dt
    diff = diff - timedelta(seconds=28800)
    total_seconds = diff.total_seconds()
    if total_seconds > 0:
        if total_seconds < 10800:  # 3 小时内
            periods = (
                (diff.seconds / 3600, '小时'),
                (diff.seconds / 60, '分钟'),
                (diff.seconds, '秒'),
            )
            for period, unit in periods:
                if period > 0:
                    return '%d%s前' % (period, unit)
            return default
        elif total_seconds < 86400 and dt.day == now.day:  # 严格的今天内
            return '今天 ' + dt.strftime('%H:%M')
        else:
            return unicode(dt.strftime('%Y-%m-%d %H:%M'))
    else:
        return default  # 别手贱写未来了...
