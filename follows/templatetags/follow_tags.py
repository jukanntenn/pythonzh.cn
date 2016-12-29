from django.template import Library
from django.contrib.contenttypes.models import ContentType

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
