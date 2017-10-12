import datetime

from wechatpy import WeChatClient

from lib.utils.sql_help import MySQL
from goal.settings import *


def subcribe_save_openid(openid):
    is_usr_exist = is_weixin_usr_exist(openid)
    if not is_usr_exist:
        mysql = MySQL(db='goal')
        create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        mysql.exec_none_query('insert into customer (id, weixin_number, create_time) values({0}, "{1}", "{2}")'.format(id, openid, create_time))


def is_weixin_usr_exist(openid):
    mysql = MySQL(db='goal')

    results = mysql.exec_query('select weixin_number from customer where weixin_number="{0}"'.format(openid))
    if results:
        return True
    else:
        return False


def get_user_info(openid):
    client = WeChatClient(WEIXIN_APPID, WEIXIN_APPSECRET)
    user = client.user.get(openid)
    return user
