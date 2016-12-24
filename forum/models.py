from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.core import urlresolvers

from model_utils.models import TimeStampedModel, SoftDeletableModel
from taggit.managers import TaggableManager
from autoslug import AutoSlugField

from replies.models import Reply
from .mark import markdownify


class Post(TimeStampedModel, SoftDeletableModel):
    title = models.CharField('title', max_length=255)
    body = models.TextField(blank=True)
    slug = AutoSlugField(populate_from='title', max_length=255, allow_unicode=True, unique=True)
    views = models.PositiveIntegerField(default=0, editable=False)
    pinned = models.BooleanField(default=False)

    category = models.ForeignKey('categories.Category')
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    tags = TaggableManager(blank=True)
    replies = GenericRelation(Reply, object_id_field='object_pk', content_type_field='content_type')

    class Meta:
        verbose_name = 'post'
        verbose_name_plural = 'posts'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return urlresolvers.reverse('forum:detail', args=(self.pk,))

    @property
    def latest_reply(self):
        return self.replies.latest('submit_date')

    def body_html(self):
        return markdownify(self.body)

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])
