from django.utils.http import urlquote_plus
from django import template

register = template.Library()

@register.filter
def urlify(value):
    return urlquote_plus(value)