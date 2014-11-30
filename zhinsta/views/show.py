# -*- coding: utf-8 -*-

import random

from flask import request
from flask import views
from instagram import InstagramAPI

from zhinsta.models.user import ShowModel
from zhinsta.models import redis
from zhinsta.settings import OPEN_ACCESS_TOKENS
from zhinsta.utils import Pager
from zhinsta.utils import add_show
from zhinsta.utils import error_handle
from zhinsta.utils import render

members_per_page = 20


class ShowView(views.MethodView):

    @error_handle
    def get(self, time_order=False):
        q = ShowModel.query.filter_by(showable=0)
        total = q.count()
        current_page = request.args.get('page', 1)
        pager = Pager(members_per_page, total)
        pager.set_current_page(current_page)
        if time_order:
            medias =\
                (q
                 .order_by(ShowModel.date_tagged.desc())
                 .order_by(ShowModel.date_created.desc())
                 .offset(pager.offset)
                 .limit(pager.limit).all())
        else:
            mids = redis.lrange('zhinsta:show:list', pager.offset, pager.offset + pager.limit - 1)
            medias = [ShowModel.query.get(x) for x in mids]
        return render('show.html', medias=medias, pager=pager)


class RealtimeView(views.MethodView):

    def get(self):
        mode = request.args.get('hob.mode', None)       # NOQA
        challenge = request.args.get('hub.challenge', None)
        vertify_token = request.args.get('hub.vertify_token', None)  # NOQA
        if challenge:
            return challenge
        return 'error'

    def post(self):
        access_token = random.choice(OPEN_ACCESS_TOKENS)
        api = InstagramAPI(access_token=access_token)
        next_url = None
        done = False
        while not done:
            medias = api.tag_recent_media(tag_name='zhinsta',
                                          with_next_url=next_url)
            next_url = medias[1]
            for m in medias[0]:
                tmp = add_show(m)
                if tmp:
                    done = True
            if not next_url:
                break
        return 'ok'
