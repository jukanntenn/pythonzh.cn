from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils import timezone


class Follow(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='follows')

    content_type = models.ForeignKey(ContentType, related_name='follows')
    object_id = models.CharField(max_length=255)
    follow_object = GenericForeignKey()
    actor_only = models.BooleanField(default=True)
    started = models.DateTimeField(default=timezone.now)

    ftype = models.CharField(max_length=255)

    class Meta:
        unique_together = ('user', 'content_type', 'object_id', 'ftype')

    def __str__(self):
        return '%s -> %s : %s' % (self.user, self.follow_object, self.ftype)
