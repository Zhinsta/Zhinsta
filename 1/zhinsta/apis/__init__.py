# -*- coding: utf-8 -*-

from flask import Blueprint

from .user import (HelloWorldView, FollowView, LikeView,
                   IslikeView)

blueprint = Blueprint('apis', __name__)

blueprint.add_url_rule('/helloworld/',
                       view_func=HelloWorldView.as_view(b'helloworld'),
                       endpoint='helloworld')

blueprint.add_url_rule('/follow/',
                       view_func=FollowView.as_view(b'follow'),
                       endpoint='follow')

blueprint.add_url_rule('/like/',
                       view_func=LikeView.as_view(b'like'),
                       endpoint='like')

blueprint.add_url_rule('/islike/',
                       view_func=IslikeView.as_view(b'islike'),
                       endpoint='islike')
