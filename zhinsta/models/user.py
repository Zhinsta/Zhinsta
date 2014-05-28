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
                             default=datetime.now)


class FollowModel(db.Model):
    __tablename__ = 'follow'
    ukey = db.Column(db.VARCHAR(128), primary_key=True)
    follow_ukey = db.Column(db.VARCHAR(128), primary_key=True)
    username = db.Column(db.VARCHAR(255), index=True, nullable=False)
    date_created = db.Column(db.DateTime(),
                             index=True, nullable=False,
                             default=datetime.now)


class LikeModel(db.Model):
    __tablename__ = 'like'
    ukey = db.Column(db.VARCHAR(128), primary_key=True)
    media = db.Column(db.VARCHAR(128), primary_key=True)
    username = db.Column(db.VARCHAR(255), index=True, nullable=False)
    media_username = db.Column(db.VARCHAR(255), index=True, nullable=False)
    date_created = db.Column(db.DateTime(),
                             index=True, nullable=False,
                             default=datetime.now)
    

class ShowModel(db.Model):
    __tablename__ = 'show'
    mid = db.Column(db.VARCHAR(128), primary_key=True)
    pic = db.Column(db.VARCHAR(255), index=True, nullable=False)
    user_pic = db.Column(db.VARCHAR(255), index=True, nullable=False)
    ukey = db.Column(db.VARCHAR(128), index=True, nullable=False)
    username = db.Column(db.VARCHAR(255), index=True, nullable=False)
    date_created = db.Column(db.DateTime(),
                             index=True, nullable=False)
    showable = db.Column(db.Integer(), index=True, nullable=False,
                         server_default='0')
    hour_tagged = db.Column(db.Integer(), index=True, nullable=False)
    date_tagged = db.Column(db.DateTime(),
                            index=True, nullable=False,
                            default=datetime.now)


class RecommendModel(db.Model):
    __tablename__ = 'recommend'
    ukey = db.Column(db.VARCHAR(128), primary_key=True)
    pic = db.Column(db.VARCHAR(255), nullable=False)
    username = db.Column(db.VARCHAR(255), index=True, nullable=False)
    order = db.Column(db.Integer(), index=True, nullable=False)
