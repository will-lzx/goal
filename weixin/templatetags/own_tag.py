import datetime
from django import template
from goal.settings import goal_status, goal_type


register = template.Library()


def convert_time(old_time):
    print('old time', old_time)
    return (old_time + datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")


def get_goal_status(key):
    return goal_status[key]


def get_goal_type(key):
    return goal_type[key]


register.filter('convert_time', convert_time)
register.filter('get_goal_status', get_goal_status)
register.filter('get_goal_type', get_goal_type)

