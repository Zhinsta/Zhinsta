# -*- coding: utf-8 -*-

from datetime import datetime
from datetime import timedelta

from flask import views
from flask import request
from flask import session
from sqlalchemy.sql import func

from ..instagram.client import InstagramAPI

from ..settings import OPEN_ACCESS_TOKEN
from ..models.user import ShowModel
from ..models.user import LikeModel
from ..engines import db
from ..utils import error_handle
from ..utils import render
from ..utils import Pager

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
                 .order_by(ShowModel.date_created.desc())
                 .offset(pager.offset)
                 .limit(pager.limit).all())
        else:
            size = datetime.now() - timedelta(days=2)
            subquery = (db.session.query(LikeModel.media,
                                         func.count(1).label('count'))
                        .filter(LikeModel.date_created>=size)
                        .group_by(LikeModel.media).subquery())
            medias =\
                (db.session.query(ShowModel)
                 .filter(ShowModel.showable==0)
                 .outerjoin(subquery, ShowModel.mid==subquery.c.media)
                 .filter(ShowModel.mid!=None)
                 .order_by(subquery.c.count.desc())
                 .order_by(ShowModel.date_created.desc())
                 .offset(pager.offset)
                 .limit(pager.limit).all())
        return render('show.html', medias=medias, pager=pager)


class RealtimeView(views.MethodView):

    def get(self):
        mode = request.args.get('hob.mode', None)
        challenge = request.args.get('hub.challenge', None)
        vertify_token = request.args.get('hub.vertify_token', None)
        if challenge:
            return challenge
        return 'error'

    def post(self):
        api = InstagramAPI(access_token=OPEN_ACCESS_TOKEN)
        next_url = None
        done = False
        while not done:
            medias = api.tag_recent_media(tag_name='zhinsta',
                                          with_next_url=next_url)
            next_url = medias[1]
            for m in medias[0]:
                showm = ShowModel.query.get(m.id)
                if showm:
                    done = True
                else:
                    showm = ShowModel(mid=m.id,
                                      pic=m.images['low_resolution'].url,
                                      user_pic=m.user.profile_picture,
                                      ukey=m.user.id,
                                      username=m.user.username,
                                      date_created=m.created_time)
                    db.session.add(showm)
                    db.session.commit()
            if not next_url:
                break
        return 'ok'
