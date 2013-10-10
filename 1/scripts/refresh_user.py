#!/usr/bin/env python

import os
import sys
import urllib
home_dir = os.path.abspath(__file__)
home_dir = home_dir[:home_dir.rindex('/')]
home_dir = home_dir[:home_dir.rindex('/')]
sys.path.insert(0, home_dir)

from zhinsta.instagram.client import InstagramAPI

from zhinsta.settings import INSTAGRAM_CLIENT_ID
from zhinsta.settings import INSTAGRAM_CLIENT_SECRET
from zhinsta.settings import INSTAGRAM_REDIRECT_URI
from zhinsta.models.user import UserModel
from zhinsta.models.user import ShowModel
from zhinsta.engines import db

api = InstagramAPI(client_id=INSTAGRAM_CLIENT_ID,
                   client_secret=INSTAGRAM_CLIENT_SECRET,
                   redirect_uri=INSTAGRAM_REDIRECT_URI)


def refresh_user_pic():
    users = UserModel.query.all()
    for user in users:
        try:
            ret = urllib.urlopen(user.pic)
            if ret.code != 200:
                api = InstagramAPI(access_token=user.access_token)
                new = api.user(user_id=user.ukey)
                user.pic = new.profile_picture
        except:
            pass
    db.session.commit()


def remove_unavailable_show_pic():
    shows = ShowModel.query.all()
    for show in shows:
        try:
            ret = urllib.urlopen(show.pic)
            if ret.code != 200:
                show.showable = 1
        except:
            pass
    db.session.commit()


def main():
    refresh_user_pic()
    remove_unavailable_show_pic()


if __name__ == '__main__':
    main()
