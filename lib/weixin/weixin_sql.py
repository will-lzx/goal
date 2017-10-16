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


def savegoal(author, goal_type, penalty, audience, period, goal_content, status):
    mysql = MySQL(db='goal')
    create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    mysql.exec_none_query(
        'insert into goal_list (author, goal_type, content, penalty, audience, frequent, status, create_time) values("{0}", "{1}", "{2}", "{3}", "{4}", "{5}", {6}, "{7}")'.format(author, goal_type, goal_content, penalty, audience, period, status, create_time))


def get_goals(openid):
    mysql = MySQL(db='goal')

    results = mysql.exec_query('select * from goal_list where author="{0}"'.format(openid))

    return results


def get_goal_by_id(goal_id):
    mysql = MySQL(db='goal')

    goal = mysql.exec_query('select * from goal_list where id={0}'.format(goal_id))
    return goal
