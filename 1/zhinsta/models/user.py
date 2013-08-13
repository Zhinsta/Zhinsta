# -*- coding: utf-8 -*-

from datetime import datetime

from ..engines import db


class UserModel(db.Model):
    __tablename__ = 'user'
    ukey = db.Column(db.VARCHAR(255), primary_key=True)
    access_token = db.Column(db.VARCHAR(255), index=True, nullable=False)
    username = db.Column(db.VARCHAR(255), index=True, nullable=False)
    pic = db.Column(db.VARCHAR(255), index=True, nullable=False)
    date_created = db.Column(db.DateTime(),
                             index=True, nullable=False,
                             default=datetime.now())


class FollowModel(db.Model):
    __tablename__ = 'follow'
    ukey = db.Column(db.VARCHAR(128), primary_key=True)
    follow_ukey = db.Column(db.VARCHAR(128), primary_key=True)
    date_created = db.Column(db.DateTime(),
                             index=True, nullable=False,
                             default=datetime.now())


class LikeModel(db.Model):
    __tablename__ = 'like'
    ukey = db.Column(db.VARCHAR(128), primary_key=True)
    media = db.Column(db.VARCHAR(128), primary_key=True)
    date_created = db.Column(db.DateTime(),
                             index=True, nullable=False,
                             default=datetime.now())
