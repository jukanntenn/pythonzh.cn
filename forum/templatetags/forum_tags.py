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

from categories.models import Category
from ..models import Post
from ..utils import parse_nicknames, bleach_value, mark, get_ctype_pk

register = template.Library()

register.filter('bleach', bleach_value)
register.filter('mark', mark)
register.filter('parse_nicknames', parse_nicknames)
register.filter('get_ctype_pk', get_ctype_pk)

register.simple_tag(get_ctype_pk, name='get_ctype_pk')


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
def action(obj):
    verb = obj.verb
    tmpl = getattr(settings, 'ACTION_TEMPLATES')[verb]
    context = {
        'actor': obj.actor,
        'target': obj.target,
        'action_object': obj.action_object,
        'timestamp': obj.timestamp
    }
    return render_to_string(tmpl, context=context)


@register.filter
def feed(obj):
    verb = obj.verb
    tmpl = getattr(settings, 'FEED_TEMPLATES')[verb]
    context = {
        'actor': obj.actor,
        'target': obj.target,
        'action_object': obj.action_object,
        'timestamp': obj.timestamp
    }
    return render_to_string(tmpl, context=context)
