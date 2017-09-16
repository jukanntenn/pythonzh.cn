import re
import datetime

import timeago

from django import template
from django.db.models import Count
from django.conf import settings
from django.db.models import Max
from django.utils.timezone import now, timedelta
from django.template.loader import render_to_string

from actstream.models import Follow

from categories.models import Category
from users.models import User
from ..models import Post
from ..utils import parse_nicknames, bleach_value, markdown_value

register = template.Library()

register.filter('bleach', bleach_value)
register.filter('mark', markdown_value)
register.filter('parse_nicknames', parse_nicknames)


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
    return Category.objects.filter(show=True).order_by('rank')


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


@register.simple_tag
def get_follow_count(obj, follow_type=None):
    return Follow.objects.followers_qs(actor=obj, follow_type=follow_type).count()


@register.simple_tag
def get_user_total_praised(user):
    replies = user.reply_comments.all()
    total = 0

    for reply in replies:
        total += Follow.objects.followers_qs(reply, follow_type='praise').count()

    return total


@register.simple_tag
def get_user_total_recommended(user):
    posts = user.post_set.all()
    total = 0

    for post in posts:
        total += Follow.objects.followers_qs(post, follow_type='recommend').count()

    return total


@register.simple_tag
def get_user_total_favorited(user):
    posts = user.post_set.all()
    total = 0

    for post in posts:
        total += Follow.objects.followers_qs(post, follow_type='favorite').count()

    return total


@register.simple_tag
def new_members(num=5):
    return User.objects.order_by('-date_joined')[:num]


@register.filter("timeago")
def timeago_filter(value):
    now_ = now()
    return timeago.format(value, now_, 'zh_CN')
