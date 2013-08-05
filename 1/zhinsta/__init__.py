# -*- coding: utf-8 -*-

from flask import Flask

from . import views
from .app import app
import filters

app.register_blueprint(views.blueprint)
