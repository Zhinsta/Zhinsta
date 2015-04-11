# -*- coding: utf-8 -*-

import gevent

from flask import views
from flask import request
from instagram import InstagramAPI
from instagram import InstagramAPIError

from zhinsta.app import app
from zhinsta.utils import error_handle
from zhinsta.utils import isfollow as is_follow
from zhinsta.utils import login_required
from zhinsta.utils import notfound
from zhinsta.utils import open_visit
from zhinsta.utils import render
from zhinsta.utils import spawn
from zhinsta.utils import get_errors

from .forms import MediaCommentForm

members_per_page = 48


class MediaProfileView(views.MethodView):

    def _get_media(self, api, mid):
        media = spawn(api.media, mid)
        likes = spawn(api.media_likes, media_id=mid)
        gevent.joinall([media, likes])
        media, likes = media.get(), likes.get()
        errors = get_errors(media, likes)
        if errors:
            if any([e.error_type == 'APINotAllowedError' for e in errors]):
                return render('profile-noauth.html', ukey=request.ukey)
            app.logger.error([str(e) for e in errors])
            return notfound(u'服务器暂时出问题了')

        ukey = media.user.id
        isfollow = False
        if request.ukey:
            try:
                isfollow = is_follow(ukey, api)
            except InstagramAPIError:
                return notfound(u'服务器暂时出问题了')

        isstar = False
        for i in likes:
            if request.ukey and request.ukey == i.id:
                isstar = True

        isme = False
        if request.ukey and ukey == request.ukey:
            isme = True
        return dict(media=media, isme=isme, isfollow=isfollow,
                    likes=likes[:5], isstar=isstar)

    @error_handle
    @open_visit
    @login_required
    def get(self, mid):
        api = InstagramAPI(access_token=request.access_token)
        media_info = self._get_media(api, mid)
        form = MediaCommentForm()
        return render('media.html', form=form, **media_info)

    @error_handle
    @login_required
    def post(self, mid):
        api = InstagramAPI(access_token=request.access_token)
        form = MediaCommentForm()
        if not form.validate():
            media_info = self._get_media(api, mid)
            return render('media.html', form=form, **media_info)
        api.create_media_comment(media_id=mid, text=form.content.data)
        media_info = self._get_media(api, mid)
        return render('media.html', form=form, **media_info)


class TagView(views.MethodView):

    @error_handle
    @open_visit
    @login_required
    def get(self, name):
        next_url = request.args.get('next_url', None)

        api = InstagramAPI(access_token=request.access_token)
        tag = api.tag(name)
        media = api.tag_recent_media(tag_name=name,
                                     with_next_url=next_url)
        tag = gevent.spawn(api.tag, name)
        media = gevent.spawn(api.tag_recent_media,
                             tag_name=name, with_next_url=next_url)
        gevent.joinall([tag, media])
        try:
            tag, media = tag.get(), media.get()
        except InstagramAPIError:
            return notfound(u'服务器暂时出问题了')

        next_url = media[1]
        media = media[0]
        return render('tag.html', tag=tag, media=media, next_url=next_url)
