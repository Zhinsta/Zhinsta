# -*- coding: utf-8 -*-

from flask import views


class HomeView(views.MethodView):

    def get(self):
        return 'ok!'
