import time

from wechatpy import WeChatClient

from lib.utils.url_request import *


def create_timestamp():
    return int(time.time())


def get_user_base_info(openid):
    access_token = get_access_token()
    url = 'https://api.weixin.qq.com/cgi-bin/user/info?access_token={0}&openid={1}&lang=zh_CN'.format(
        access_token, openid)

    url_req = UrlRequest()
    resp = url_req.url_request(url)
    return resp


def get_access_token():
    mysql = MySQL(db='goal')
    access_token = mysql.exec_query('select token from access_token WHERE id=1')[0][0]
    return access_token


def get_user_info(openid):
    client = WeChatClient(WEIXIN_APPID, WEIXIN_APPSECRET)
    user = client.user.get(openid)
    return user
