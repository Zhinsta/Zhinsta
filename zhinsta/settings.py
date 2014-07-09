# -*- coding: utf-8 -*-

try:
    from zhinsta.settings_local import *  # NOQA
except ImportError:
    print 'local settings not found'
    pass

try:
    import sae.const

    SECRET_KEY = 'SteinsGate'   # 生产环境应该保密
    MYSQL_DB = sae.const.MYSQL_DB
    MYSQL_USER = sae.const.MYSQL_USER
    MYSQL_PASS = sae.const.MYSQL_PASS
    MYSQL_HOST = sae.const.MYSQL_HOST
    MYSQL_HOST_S = sae.const.MYSQL_HOST_S
    MYSQL_PORT = sae.const.MYSQL_PORT
    INSTAGRAM_CLIENT_ID = 'f89feb5623484adf9347b12c845af9aa'
    INSTAGRAM_CLIENT_SECRET = '8f0479ee76c548889200612149cd8633'
    INSTAGRAM_REDIRECT_URI = 'http://zhinsta.sinaapp.com/instagram/redirect/'
except ImportError:
    SECRET_KEY = 'SteinsGate'   # 生产环境应该保密
    MYSQL_DB = 'zhinsta'
    MYSQL_USER = 'root'
    MYSQL_PASS = ''
    MYSQL_HOST = '127.0.0.1'
    MYSQL_PORT = '3306'
    INSTAGRAM_CLIENT_ID = '30fc02241ccb410fbf7fe5508c650c78'
    INSTAGRAM_CLIENT_SECRET = '28ede58b51f94de594b3af4b3fff1a1f'
    INSTAGRAM_REDIRECT_URI = 'http://www.dev.zhinsta.com:5000/instagram/redirect/'

INSTAGRAM_SCOPE = ['comments', 'relationships', 'likes']
OPEN_ACCESS_TOKENS = [
    '524431895.30fc022.4da293d4ccf044489f3f495727343a31',
]
