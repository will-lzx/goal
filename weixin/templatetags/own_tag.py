import datetime
from django import template
from goal.settings import goal_status



register = template.Library()


def convert_time(old_time):
    return (old_time + datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")


def get_goal_status(key):
    return goal_status[key]


register.filter('convert_time', convert_time)
register.filter('get_goal_status', get_goal_status)

