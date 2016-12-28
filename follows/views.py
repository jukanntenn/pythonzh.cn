from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.contenttypes.models import ContentType

from actstream.views import respond

from .actions import follow, unfollow


@login_required
@csrf_exempt
def follow_unfollow(request, content_type_id, object_id, ftype, do_follow=True, actor_only=True):
    ctype = get_object_or_404(ContentType, pk=content_type_id)
    instance = get_object_or_404(ctype.model_class(), pk=object_id)

    if do_follow:
        follow(request.user, instance, ftype, actor_only=actor_only)
        return respond(request, 201)  # CREATED
    unfollow(request.user, instance, ftype)
    return respond(request, 204)  # NO CONTENT
