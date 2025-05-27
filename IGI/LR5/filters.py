from django import template
from calendar import *
from datetime import datetime
import zoneinfo

register = template.Library()

@register.filter
def multiply_by_100(value):
    value = value * 100
    value = int(value)
    return value

@register.filter
def print_calendar(value):
    value = datetime.now(zoneinfo.ZoneInfo(value))
    month = value.month
    year = value.year

    cal = TextCalendar()
    cal = cal.formatmonth(year,month)

    return cal