# -*- coding: utf-8 -*-

from flask import Blueprint
from flask.ext.restful import Api

from .user import HelloWorldView, FollowView
from .media import LikeView, IslikeView, CommentView

blueprint = Blueprint('apis', __name__)

api = Api(blueprint)

api.add_resource(HelloWorldView, '/helloworld')

blueprint.add_url_rule('/follow/',
                       view_func=FollowView.as_view(b'follow'),
                       endpoint='follow')

blueprint.add_url_rule('/like/',
                       view_func=LikeView.as_view(b'like'),
                       endpoint='like')

blueprint.add_url_rule('/islike/',
                       view_func=IslikeView.as_view(b'islike'),
                       endpoint='islike')

blueprint.add_url_rule('/comment/',
                       view_func=CommentView.as_view(b'comment'),
                       endpoint='comment')
