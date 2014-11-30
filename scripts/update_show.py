# coding: utf-8

import time

import redis
from sqlalchemy.sql import expression
from sqlalchemy.sql import func

from zhinsta.engines import db
from zhinsta.models.user import LikeModel
from zhinsta.models.user import ShowModel

KEY = "zhinsta:show:list"


def generate_show():
    subquery = (db.session.query(LikeModel.media,
                                 func.count(1).label('count'))
                .group_by(LikeModel.media).subquery())
    now = int(time.time() / 7200)
    order = expression.label('hacker', (subquery.c.count + 1.0) / (now - ShowModel.hour_tagged + 2.0) / (now - ShowModel.hour_tagged + 2.0))
    medias =\
        (db.session.query(ShowModel)
         .filter(ShowModel.showable == 0)
         .outerjoin(subquery, ShowModel.mid == subquery.c.media)
         .filter(ShowModel.mid != None)     # NOQA
         .order_by(order.desc())
         .order_by(ShowModel.date_tagged.desc())
         .order_by(ShowModel.date_created.desc())
         .all())
    return [x.mid for x in medias]


def update_redis():
    pipe = redis.Redis().pipeline()
    pipe.delete(KEY)
    mids = generate_show()
    pipe.rpush(KEY, *mids)
    pipe.execute()
    return len(mids)

if __name__ == '__main__':
    while True:
        count = update_redis()
        print 'updated! total {} items in show list.'.format(count)
        time.sleep(60 * 5)
