from django.db import models
from django.db.models import Max
from django.db.models.functions import Coalesce
from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.core import urlresolvers
from django.utils.translation import ugettext_lazy as _

from model_utils.models import TimeStampedModel, SoftDeletableModel
from model_utils.managers import SoftDeletableQuerySet
from taggit.managers import TaggableManager
from autoslug import AutoSlugField

from replies.models import Reply


class PostQuerySet(SoftDeletableQuerySet):
    def visible(self):
        return self.filter(is_removed=False, category__is_removed=False)

    def ordered(self):
        return self.annotate(
            latest_reply_time=Coalesce(Max('replies__submit_date'), 'created')).order_by(
            '-pinned',
            '-latest_reply_time')


class PostManager(models.Manager):
    pass


class Post(TimeStampedModel, SoftDeletableModel):
    title = models.CharField(_('title'), max_length=255)
    body = models.TextField(_('body'), blank=True)
    slug = AutoSlugField(_('slug'), populate_from='title', max_length=255, allow_unicode=True, unique=True)
    views = models.PositiveIntegerField(_('views'), default=0, editable=False)
    pinned = models.BooleanField(_('pinned'), default=False)

    category = models.ForeignKey('categories.Category', verbose_name=_('category'))
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('author'))
    tags = TaggableManager(blank=True, verbose_name=_('tags'))
    replies = GenericRelation(Reply, object_id_field='object_pk', content_type_field='content_type',
                              verbose_name=_('replies'))

    objects = PostManager.from_queryset(PostQuerySet)()

    class Meta:
        verbose_name = _('post')
        verbose_name_plural = _('posts')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return urlresolvers.reverse('forum:detail', args=(self.pk,))

    def latest_reply(self):
        return self.replies.latest('submit_date')

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])
