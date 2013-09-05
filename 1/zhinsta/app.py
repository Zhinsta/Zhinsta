# -*- coding: utf-8 -*-

from datetime import timedelta

from flask import Flask
from flask import session

from .settings import SECRET_KEY

app = Flask(__name__)
app.secret_key = SECRET_KEY
session.permanent = True
app.permanent_session_lifetime = timedelta(days=30)
