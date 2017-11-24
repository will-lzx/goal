import datetime
from django import template
from goal.settings import goal_status, goal_type
from lib.utils.common import get_user_base_info
from lib.weixin.weixin_sql import get_goals_rank, get_goal_by_id, get_audience
from lib.utils.sql_help import MySQL

register = template.Library()


def convert_time(old_time):
    print('old time', old_time)
    return (old_time + datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")


def get_goal_status(key):
    return goal_status[key]


def get_goal_owner(goal_id):
    goal = get_goal_by_id(goal_id)
    return goal[0][1]


def get_goal_current_status(goal_id):
    goal = get_goal_by_id(goal_id)
    return goal_status[goal[0][6]]


def get_goal_content(goal_id):
    goal = get_goal_by_id(goal_id)
    return goal[0][3]


def get_goal_audience_count(goal_id):

    audiences = get_audience(goal_id)
    return len(audiences)


def get_goal_create_time(goal_id):

    goal = get_goal_by_id(goal_id)
    return (goal[0][7] + datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")


def get_goal_type(key):
    return goal_type[key]


def get_author_name(open_id):
    user_info = get_user_base_info(open_id)
    return user_info['nickname']


def get_headimg(open_id):
    user_info = get_user_base_info(open_id)
    return user_info['headimgurl']


def get_rank(open_id):
    goal_rank_dict, sort_values = get_goals_rank()
    return sort_values.index(open_id) + 1


def get_goal_onging(open_id):
    mysql = MySQL(db='goal')

    count = mysql.exec_query('select count(*) from goal_list where author="{0}" and status=0'.format(open_id))[0][0]

    return count


def get_goal_complete(open_id):
    mysql = MySQL(db='goal')

    count = mysql.exec_query('select count(*) from goal_list where author="{0}" and status=1'.format(open_id))[0][0]

    return count


def get_goal_giveup(open_id):
    mysql = MySQL(db='goal')

    count = mysql.exec_query('select count(*) from goal_list where author="{0}" and status=2'.format(open_id))[0][0]

    return count


def get_goal_count(open_id):
    mysql = MySQL(db='goal')

    count = mysql.exec_query('select count(*) from goal_list where author="{0}"'.format(open_id))[0][0]

    return count


register.filter('convert_time', convert_time)
register.filter('get_goal_status', get_goal_status)
register.filter('get_goal_type', get_goal_type)
register.filter('get_author_name', get_author_name)
register.filter('get_headimg', get_headimg)
register.filter('get_rank', get_rank)

register.filter('get_goal_onging', get_goal_onging)


register.filter('get_goal_complete', get_goal_complete)

register.filter('get_goal_giveup', get_goal_giveup)

register.filter('get_goal_count', get_goal_count)

register.filter('get_goal_content', get_goal_content)

register.filter('get_goal_audience_count', get_goal_audience_count)

register.filter('get_goal_create_time', get_goal_create_time)

register.filter('get_goal_current_status', get_goal_current_status)

register.filter('get_goal_owner', get_goal_owner)




