import os
import sys
sys.path.insert(0, os.getcwd())

from instagram import InstagramAPI

from zhinsta.settings import INSTAGRAM_CLIENT_ID
from zhinsta.settings import INSTAGRAM_CLIENT_SECRET
from zhinsta.settings import INSTAGRAM_REDIRECT_URI

api = InstagramAPI(client_id=INSTAGRAM_CLIENT_ID,
                   client_secret=INSTAGRAM_CLIENT_SECRET,
                   redirect_uri=INSTAGRAM_REDIRECT_URI)


def main():
    print api.list_subscriptions()


if __name__ == '__main__':
    main()
