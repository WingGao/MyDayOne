__author__ = 'wing'
from django import template
from Dayone.models_mongo import TAG_DAY_CN
import datetime
register = template.Library()


@register.filter(name='tag_day_type')
def tag_day_type(daytype):
    return TAG_DAY_CN[daytype]

@register.filter
def daysince(date):
    return (datetime.datetime.now() - date).days
