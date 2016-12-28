from django.template import Library

from .. import actions

register = Library()


@register.simple_tag
def is_following(user, obj, ftype):
    return actions.is_following(user, obj, ftype)
