# -*- coding: utf-8 -*-

import datetime
import io
from urllib import request
from urllib.request import urlopen

from wechatpy import WeChatClient

from lib.utils.common import sort_by_value
from lib.utils.sql_help import MySQL
from goal.settings import *

import pymysql
pymysql.install_as_MySQLdb()


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


def savegoal(author, goal_type, penalty, period, goal_content, status):
    mysql = MySQL(db='goal')
    create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    mysql.exec_none_query(
        'insert into goal_list (author, goal_type, content, penalty, frequent, status, create_time) values("{0}", "{1}", "{2}", "{3}", "{4}", {5}, "{6}")'.format(author, goal_type, goal_content, penalty, period, status, create_time))

    sql = 'select id from goal_list where author = "{0}" and create_time="{1}"'.format(author, create_time)

    mysql = MySQL(db='goal')
    goal_id = mysql.exec_query(sql)[0][0]
    return goal_id


def get_goals(openid):
    mysql = MySQL(db='goal')

    results = mysql.exec_query('select * from goal_list where author="{0}" order by create_time DESC'.format(openid))

    return results


def get_goals_rank():
    mysql = MySQL(db='goal')

    results = mysql.exec_query('select author from goal_list')
    author_count_dict = {}

    for result in results:
        if author_count_dict.keys().__contains__(result[0]):
            author_count_dict[result[0]] = author_count_dict[result[0]] + 1
        else:
            author_count_dict[result[0]] = 1
    return author_count_dict, sort_by_value(author_count_dict)


def get_goal_id():
    mysql = MySQL(db='goal')

    goal_id = mysql.exec_query('select LAST_INSERT_ID()')[0][0]

    return goal_id


def get_goal_by_id(goal_id):

    print('verify goal id ', goal_id)
    mysql = MySQL(db='goal')

    goal = mysql.exec_query('select * from goal_list where id={0}'.format(goal_id))
    return goal


def get_audience(goal_id):
    mysql = MySQL(db='goal')

    goal_audience_list = mysql.exec_query('select audience from goal_audience_relation where goal_id={0}'.format(goal_id))
    return goal_audience_list


def save_goal_history(goal_id, content, image_files):
    mysql = MySQL(db='goal')
    create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    mysql.exec_none_query('insert into goal_history (goal_id, content, create_time) values({0}, "{1}", "{2}")'.format(goal_id, content, create_time))

    sql = 'select id from goal_history where goal_id = "{0}" and create_time="{1}"'.format(goal_id, create_time)

    mysql = MySQL(db='goal')
    history_id = mysql.exec_query(sql)[0][0]

    index = 1
    for f in image_files:
        save_history_image(history_id, f, index)
        index += 1

    #image_urls = image_url.split(';')
    # for url in image_urls:
    #     if url:
    #         print('ur;', url)
    #         print('index', index)
    #         save_history_image(history_id, url, index)
    #         index += 1


def save_history_image(history_id, image_url, index):
    mysql = MySQL(db='goal')

    create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # try:
    #     data = urlopen(image_url).read()
    # except Exception as ex:
    #     print('image_url', image_url)
    #     print(ex)

    #data_stream = io.BytesIO(image_bytes)

    try:
        # f = open(image_url, 'rb')
        # data = f.read()
        # f.close()
        data = image_url.read()
    except Exception as ex:
        print('image_url', image_url)
        print(ex)

    sql = 'insert into history_image_url (history_id, data, image_index, create_time) values(%s, %s, %s, %s)'
    arg = (history_id, data, index, create_time)
    print('sql', sql)
    mysql.exec_none_query(sql, arg)


def get_history_image(history_id, index):
    mysql = MySQL(db='goal')

    data = mysql.exec_query('select data from history_image_url where history_id={0} and index={1}'.format(history_id, index))

    return data[0][0]


def get_goal_history(goal_id):
    mysql = MySQL(db='goal')

    goal_history = mysql.exec_query('select * from goal_history where goal_id={0}'.format(goal_id))
    return goal_history


def get_history_images(history_id):
    mysql = MySQL(db='goal')

    history_images = mysql.exec_query('select * from history_image_url where history_id={0}'.format(history_id))
    return history_images


def update_goal(goal_id, action):
    mysql = MySQL(db='goal')

    try:
        mysql.exec_none_query('update goal_list set status={0} where id={1}'.format(action, goal_id))
        return True
    except:
        print('Goal {0} status update fail'.format(goal_id))
        return False


def modify_audience(goal_id, open_id, action):
    mysql = MySQL(db='goal')
    create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if action == 'create':
        sql = 'insert into goal_audience_relation (goal_id, audience, create_time) values("{0}", "{1}", "{2}")'.format(goal_id, open_id, create_time)
    elif action == 'remove':
        sql = 'delete from goal_audience_relation where goal_id="{0}" and audience="{1}"'.format(goal_id, open_id)

    try:
        mysql.exec_none_query(sql)
        return True
    except:
        print('Goal {0} status update fail'.format(goal_id))
        return False


def get_audience_goals(open_id):
    mysql = MySQL(db='goal')

    audience_goals = mysql.exec_query('select * from goal_audience_relation where audience="{0}" order by create_time DESC'.format(open_id))
    return audience_goals


if __name__ == '__main__':
    save_history_image(1, 'http://mgoal.cn/static/images/kanshu.jpg', 1)

    print('')
