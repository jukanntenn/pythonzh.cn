import re
import datetime

from django import template
from django.db.models import Count, DateTimeField
from django.conf import settings
from django.utils.html import mark_safe
from django.db.models import Max
from django.db.models.functions import Coalesce
from django.utils.timezone import now, timedelta
from django.template.loader import render_to_string
from django.contrib.contenttypes.models import ContentType

import bleach

from categories.models import Category
from ..models import Post
from ..mark import markdownify
from ..utils import parse_nicknames

register = template.Library()


@register.simple_tag
def get_popular_posts():
    q = Post.objects.annotate(
        num_replies=Count('replies'),
        latest_reply_time=Max('replies__submit_date')
    ).filter(
        num_replies__gt=0,
        latest_reply_time__gt=(now() - datetime.timedelta(days=1)),
        latest_reply_time__lt=now()
    ).order_by('-num_replies', '-latest_reply_time')[:10]
    return q


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


@register.filter
def describe(obj):
    verb = obj.verb
    tmpl = getattr(settings, 'NOTIFICATION_TEMPLATES')[verb]
    context = {
        'notification': obj,
        'actor': obj.actor,
        'action_obj': obj.action_object,
        'target': obj.target,
    }
    return render_to_string(tmpl, context=context)


@register.filter
def mark(value):
    return markdownify(value)


@register.filter(name='parse_nicknames')
def parse_nicknames_filter(value):
    return parse_nicknames(value)


@register.filter
def ctype_id(obj):
    return ContentType.objects.get_for_model(obj).pk
