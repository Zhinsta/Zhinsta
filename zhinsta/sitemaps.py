# -*- coding: utf-8 -*-
from __future__ import unicode_literals
"""Sitemap 模块"""

from datetime import datetime
from collections import namedtuple

from werkzeug.utils import cached_property
from flask import (views, render_template,
                   Response, request, url_for)
from .utils import Pager


class SitemapEntry(
    namedtuple(
        'SitemapEntry',
        'location lastmod changefreq priority originality title '
        'date_created source category author image')):
    def __new__(
            cls, location, lastmod=None, changefreq='always',
            priority=.5, originality=0, title=None, date_created=None,
            source=None, category=None, author=None, image=None):
        if lastmod is None:
            lastmod = datetime.now()
        if date_created is None:
            date_created = lastmod
        return super(SitemapEntry, cls).__new__(
            cls, location, lastmod, changefreq,
            priority, originality, title, date_created,
            source, category, author, image)


class SitemapView(views.View):
    # This limit (50000) is defined by Google. See the index documentation at
    # http://sitemaps.org/protocol.php#index.
    # 因为百度原创联盟还要取一堆奇怪的数据, 为降低内存压力, 改成 10000 条一页
    limit = 10000
    limit_debug = 1000
    entry_class = SitemapEntry
    sitemap_template = 'sitemap/sitemap.xml'
    sitemap_index_template = 'sitemap/sitemap_index.xml'

    def get_objects_count(self):
        """在这里实现获取对象长度的方法

        Returns
            integer

        """
        raise NotImplementedError

    def get_objects(self, offset, limit, **kwargs):
        """在这里实现获取对象的方法

        Returns
            [SitemapEntry(), ...]

        """
        raise NotImplementedError

    def context(self):
        return self.special_args

    def sitemap(self):
        items = []
        limit = self.limit
        pager = Pager(limit, self.get_objects_count())
        kwargs = self.special_args
        for item in self.get_objects(pager.current_offset,
                                     pager.limit, **kwargs):
            items.append(item)
        return Response(
            render_template(self.sitemap_template,
                            items=items, **self.context()),
            mimetype='application/xml')

    @cached_property
    def special_args(self):
        kwargs = {}
        if 'baiducustom' in request.args:
            kwargs['baiducustom'] = request.args['baiducustom'] or 'y'
            if 'open' in request.args:
                kwargs['open'] = request.args['open'].lower() != 'false'
        return kwargs

    def sitemap_index(self):
        limit = self.limit
        if self.debug:
            limit = self.limit_debug
        print '*' * 100
        print self.get_objects_count()
        pager = Pager(limit, self.get_objects_count())
        sitemaps = []
        kwargs = self.special_args
        for i in xrange(1, pager.total_page + 1):
            sitemaps.append(url_for(request.endpoint, page=i,
                                    _external=True, **kwargs))
        return Response(
            render_template(self.sitemap_index_template,
                            sitemaps=sitemaps, **self.context()),
            mimetype='application/xml')

    def dispatch_request(self):
        if 'index' in request.args:
            return self.sitemap_index()
        else:
            return self.sitemap()
