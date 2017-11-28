import time

from wechatpy import WeChatClient

from lib.utils.url_request import *


def create_timestamp():
    return int(time.time())


def get_user_base_info(openid):
    access_token = get_access_token()
    url = 'https://api.weixin.qq.com/cgi-bin/user/info?access_token={0}&openid={1}&lang=zh_CN'.format(
        access_token, openid)

    print('url is,', url)

    url_req = UrlRequest()
    resp = url_req.url_request(url)
    return resp


def is_subscribe(openid):
    resp = get_user_base_info(openid)

    if resp['subscribe'] == 0:
        return False
    return True


def get_access_token():
    mysql = MySQL(db='goal')
    access_token = mysql.exec_query('select token from access_token WHERE id=1')[0][0]
    return access_token


def get_openid(code):
    url = 'https://api.weixin.qq.com/sns/oauth2/access_token?appid={0}&secret={1}&code={2}&grant_type=authorization_code'.format(
        WEIXIN_APPID, WEIXIN_APPSECRET, code)

    url_req = UrlRequest()
    resp = url_req.url_request(url)
    return resp['openid']


def is_own_goal(open_id, goal_id):
    if open_id == goal_id:
        return True
    else:
        return False


def sort_by_value(d):
    items = d.items()
    backitems = [[v[1], v[0]] for v in items]
    backitems.sort()
    return [backitems[i][1] for i in range(0, len(backitems))]
