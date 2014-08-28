# -*- coding: utf-8 -*-

from flask import Flask  # NOQA

from zhinsta import views
from zhinsta import apis
from zhinsta.admin import zhinsta_admin
from zhinsta.app import app
import filters           # NOQA

zhinsta_admin.init_app(app)

app.debug = False
app.register_blueprint(views.blueprint)
app.register_blueprint(apis.blueprint, url_prefix='/apis')
