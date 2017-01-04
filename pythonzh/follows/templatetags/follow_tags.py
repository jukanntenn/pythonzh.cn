from django.template import Library
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.template.loader import render_to_string

from .. import actions
from ..models import Follow

register = Library()


@register.simple_tag
def is_following(user, obj, ftype):
    if user.is_anonymous:
        return False
    return actions.is_following(user, obj, ftype)


@register.filter
def follower_count(obj, ftype):
    ctype = ContentType.objects.get_for_model(obj)
    return Follow.objects.filter(content_type=ctype, object_id=obj.pk, ftype=ftype).count()


@register.filter
def follow(obj):
    ftype = obj.ftype
    tmpl = getattr(settings, 'FOLLOW_TEMPLATES')[ftype]
    context = {
        'follow': obj,
        'follow_object': obj.follow_object,
    }
    return render_to_string(tmpl, context=context)
