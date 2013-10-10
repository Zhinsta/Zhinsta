import os
import sys
import urllib
sys.path.insert(0, os.getcwd())

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
        ret = urllib.urlopen(user.pic)
        if ret.code != 200:
            api = InstagramAPI(access_token=user.access_token)
            new = api.user(user_id=user.ukey)
            user.pic = new['profile_picture']
    db.session.commit()


def remove_unavailable_show_pic():
    shows = ShowModel.query.all()
    for show in shows:
        ret = urllib.urlopen(show.pic)
        if ret.code != 200:
            show.showable = 1
    db.session.commit()


def main():
    refresh_user_pic()
    remove_unavailable_show_pic()


if __name__ == '__main__':
    main()
