# coding=utf-8
__author__ = 'wing'
from django import template
from Dayone.models_mongo import TAG_DAY_CN, TAG_DAY
import datetime
import markdown

register = template.Library()


@register.filter(name='tag_day_type')
def tag_day_type(daytype):
    return TAG_DAY_CN[daytype]


@register.filter
def daysince(date):
    return (datetime.datetime.now() - date).days


@register.filter
def tagurl(tname):
    t = tname.split('-', 1)
    if len(t) == 2 and t[0] in TAG_DAY:
        return '/day/all'
    else:
        return '/tag/' + tname


@register.filter
def cnweek(day):
    return '周' + ['一', '二', '三', '四', '五', '六', '日'][day]

@register.filter
def dayone_markdown(t):
    return markdown.markdown(t)
