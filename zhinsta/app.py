# -*- coding: utf-8 -*-

import logging

logging.basicConfig(
    format='[%(levelname)1.1s %(asctime)s %(module)s:%(lineno)d] %(message)s'
)

from datetime import timedelta

from flask import Flask

from zhinsta.settings import SECRET_KEY

app = Flask(__name__)
app.secret_key = SECRET_KEY
app.permanent_session_lifetime = timedelta(days=30)


def run():
    app.run(debug=True)
