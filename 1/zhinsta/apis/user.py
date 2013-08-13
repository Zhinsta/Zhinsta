# -*- coding: utf-8 -*-

import json

from flask import views
from flask import session
from flask import request

from ..instagram.client import InstagramAPI

from ..engines import db
from ..utils import login_required
from ..utils import json_response
from ..models.user import FollowModel
from ..models.user import LikeModel


class HelloWorldView(views.MethodView):

    @login_required
    def get(self):
        ret_type = request.args.get('type', '')
        if ret_type == 'json':
            return json.dumps({'result': 'hello!'})
        if ret_type == 'string':
            return 'hello!'
        return json_response('hello!')


class FollowView(views.MethodView):

    @login_required
    def get(self):
        action = request.args.get('action', 'follow')
        ukey = request.args.get('ukey', '')
        api = InstagramAPI(access_token=session.get('access_token', ''))
        if action == 'follow':
            api.follow_user(user_id=ukey)
            m = FollowModel(ukey=session.get('ukey', ''),
                            follow_ukey=ukey)
            db.session.add(m)
        if action == 'unfollow':
            api.unfollow_user(user_id=ukey)
            m = FollowModel.query.get((session.get('ukey', ''), ukey))
            if m:
                db.session.delete(m)
        db.session.commit()
        return json_response('ok')


class LikeView(views.MethodView):

    @login_required
    def get(self):
        action = request.args.get('action', 'like')
        mid = request.args.get('mid', '')
        api = InstagramAPI(access_token=session.get('access_token', ''))
        if action == 'like':
            api.like_media(media_id=mid)
            m = LikeModel(ukey=session.get('ukey', ''), media=mid)
            db.session.add(m)
        if action == 'unlike':
            api.unlike_media(media_id=mid)
            m = LikeModel.query.get((session.get('ukey', ''), mid))
            if m:
                db.session.delete(m)
        db.session.commit()
        return json_response('ok')
