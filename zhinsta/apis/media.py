# -*- coding: utf-8 -*-

from flask import views
from flask import session
from flask import request

from flask.ext.restful import reqparse

from instagram import InstagramAPI

from ..engines import db
from ..utils import login_required
from ..utils import json_response
from ..utils import api_error_handle
from ..utils import add_show
from ..models.user import LikeModel


parser = reqparse.RequestParser()
parser.add_argument('type', type=str, help="test")


class CommentView(views.MethodView):

    @api_error_handle
    @login_required
    def get(self):
        action = request.args.get('action', 'create_comment')
        mid = request.args.get('mid', '')
        text = request.args.get('text', '')
        api = InstagramAPI(access_token=session.get('access_token', ''))
        if action == 'create_comment':
            api.create_media_comment(media_id=mid, text=text)
        elif action == 'delete_comment':
            cid = request.args.get('comment_id', '')
            api.delete_comment(media_id=mid, comment_id=cid)
        return json_response('ok')


class LikeView(views.MethodView):

    @api_error_handle
    @login_required
    def get(self):
        action = request.args.get('action', 'like')
        mid = request.args.get('mid', '')
        api = InstagramAPI(access_token=session.get('access_token', ''))
        if action == 'like':
            api.like_media(media_id=mid)
            media = api.media(mid)
            m = LikeModel(ukey=session.get('ukey', ''), media=mid,
                          username=session.get('username', ''),
                          media_username=media.user.username)
            db.session.add(m)
            add_show(media)
        if action == 'unlike':
            api.unlike_media(media_id=mid)
            m = LikeModel.query.get((session.get('ukey', ''), mid))
            if m:
                db.session.delete(m)
        db.session.commit()
        return json_response('ok')


class IslikeView(views.MethodView):

    @api_error_handle
    @login_required
    def get(self):
        mid = request.args.get('mid', '')
        ukey = session.get('ukey', '')
        api = InstagramAPI(access_token=session.get('access_token', ''))
        likes = api.media_likes(media_id=mid)
        ret = False
        for i in likes:
            if ukey == i.id:
                ret = True
                break
        return json_response(ret)
