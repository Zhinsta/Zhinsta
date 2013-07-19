# -*- coding: utf-8 -*-

from flask import Blueprint

from .home import HomeView

blueprint = Blueprint('view', __name__)

blueprint.add_url_rule('/',
                       view_func=HomeView.as_view(b'home'),
                       endpoint='home')
