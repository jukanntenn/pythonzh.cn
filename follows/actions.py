from django.contrib.contenttypes.models import ContentType

from actstream.signals import action
from actstream.registry import check
from notifications.signals import notify

from .models import Follow


def follow(user, obj, ftype, send_action=True, actor_only=True, **kwargs):
    check(obj)
    instance, created = Follow.objects.get_or_create(
        user=user, object_id=obj.pk,
        content_type=ContentType.objects.get_for_model(obj),
        actor_only=actor_only,
        ftype=ftype)
    if send_action and created:
        action.send(user, verb=ftype, target=obj, **kwargs)

    try:
        recipient = obj.author
    except:
        recipient = obj.user

    if user != recipient:
        notify.send(sender=user, recipient=recipient, verb=ftype, target=obj)
    return instance


def unfollow(user, obj, ftype, send_action=False):
    check(obj)
    Follow.objects.filter(
        user=user, object_id=obj.pk,
        content_type=ContentType.objects.get_for_model(obj),
        ftype=ftype
    ).delete()

    if send_action:
        action.send(user, verb='un%s' % ftype, target=obj)


def is_following(user, obj, ftype):
    check(obj)
    return Follow.objects.filter(
        user=user, object_id=obj.pk,
        content_type=ContentType.objects.get_for_model(obj),
        ftype=ftype
    ).exists()
