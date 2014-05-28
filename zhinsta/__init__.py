# -*- coding: utf-8 -*-

from flask import Flask  # NOQA

from . import views
from . import apis
from .app import app
import filters           # NOQA

app.register_blueprint(views.blueprint)
app.register_blueprint(apis.blueprint, url_prefix='/apis')
