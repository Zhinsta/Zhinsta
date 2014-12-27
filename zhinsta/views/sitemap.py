# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from flask import url_for
from zhinsta.sitemaps import SitemapView
from zhinsta.engines import db

from zhinsta.models.user import UserModel, LikeModel, ShowModel


class UserSitemapView(SitemapView):

    def get_objects_count(self):
        return UserModel.query.count()

    def get_objects(self, offset, limit, **kwargs):
        users = (db.session.query(
            UserModel.ukey, UserModel.date_created).
            order_by(
                UserModel.date_created).
            offset(offset).limit(limit).all())
        return [self.entry_class(
            location=url_for('view.profile', ukey=u.ukey,
                             _external=True, **kwargs),
            lastmod=u.date_created,
            changefreq='hourly',
            priority=.7) for u in users]


class ShowSitemapView(SitemapView):

    def get_objects_count(self):
        return ShowModel.query.count()

    def get_objects(self, offset, limit, **kwargs):
        medias = (db.session.query(
            ShowModel.mid,
            ShowModel.pic,
            ShowModel.username,
            ShowModel.user_pic,
            ShowModel.date_created).
            order_by(ShowModel.date_created).
            offset(offset).limit(limit))
        return [self.entry_class(
            location=url_for('view.media', mid=m.mid,
                             _external=True, **kwargs),
            lastmod=m.date_created,
            changefreq='daily',
            priority=.9,
            originality=1,
            date_created=m.date_created,
            source=url_for('view.media', mid=m.mid,
                           _external=True, **kwargs),
            category='media page',
            author=m.username
        )for m in medias]


class LikeSitemapView(SitemapView):

    def get_objects_count(self):
        return LikeModel.query.count()

    def get_objects(self, offset, limit, **kwargs):
        medias = (db.session.query(
            LikeModel.media,
            LikeModel.media_username,
            LikeModel.date_created).
            order_by(LikeModel.date_created).
            offset(offset).limit(limit))
        return [self.entry_class(
            location=url_for('view.media', mid=m.media,
                             _external=True, **kwargs),
            lastmod=m.date_created,
            changefreq='daily',
            priority=.9,
            originality=1,
            date_created=m.date_created,
            source=url_for('view.media', mid=m.media,
                           _external=True, **kwargs),
            category='media page',
            author=m.media_username
        )for m in medias]
