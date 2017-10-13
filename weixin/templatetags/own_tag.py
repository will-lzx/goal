import datetime
from django import template


register = template.Library()


def convert_time(old_time):
    return (old_time + datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")


register.filter('convert_time', convert_time)

