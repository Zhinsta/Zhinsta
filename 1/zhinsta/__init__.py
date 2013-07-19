# -*- coding: utf-8 -*-

from flask import Flask

from . import views

app = Flask(__name__)

app.register_blueprint(views.blueprint)
