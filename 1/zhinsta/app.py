# -*- coding: utf-8 -*-

from flask import Flask

from .settings import SECRET_KEY

app = Flask(__name__)
app.secret_key = SECRET_KEY
