# -*- coding: utf-8 -*-

from flask import Flask  # NOQA

from . import views
from . import apis
from .admin import zhinsta_admin
from .app import app
import filters           # NOQA

zhinsta_admin.init_app(app)

app.register_blueprint(views.blueprint)
app.register_blueprint(apis.blueprint, url_prefix='/apis')
