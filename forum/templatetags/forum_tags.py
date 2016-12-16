from django import template
from django.db.models import Count
from django.conf import settings
from django.utils.html import mark_safe

import bleach

from categories.models import Category
from ..models import Post

register = template.Library()


@register.simple_tag
def get_popular_posts():
    return Post.objects.all().annotate(num_replies=Count('replies')).order_by('-num_replies')[:6]


@register.simple_tag
def get_categories():
    return Category.objects.filter(parent__isnull=True)


@register.simple_tag
def get_quick_categories():
    return Category.objects.filter(parent__isnull=False)


bleach_args = {}

possible_settings = {
    'BLEACH_ALLOWED_TAGS': 'tags',
    'BLEACH_ALLOWED_ATTRIBUTES': 'attributes',
    'BLEACH_ALLOWED_STYLES': 'styles',
    'BLEACH_STRIP_TAGS': 'strip',
    'BLEACH_STRIP_COMMENTS': 'strip_comments',
}

for setting, kwarg in possible_settings.items():
    if hasattr(settings, setting):
        bleach_args[kwarg] = getattr(settings, setting)


def bleach_value(value):
    bleached_value = bleach.clean(value, **bleach_args)
    return mark_safe(bleached_value)


register.filter('bleach', bleach_value)
