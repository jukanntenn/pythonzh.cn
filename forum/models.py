from django.db import models
from django.db.models import Max
from django.db.models.functions import Coalesce
from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from model_utils.models import TimeStampedModel, SoftDeletableModel
from model_utils.managers import SoftDeletableQuerySet
from taggit.managers import TaggableManager

from replies.models import Reply


class PostQuerySet(SoftDeletableQuerySet):
    def natural_order(self):
        return self.annotate(
            natural_timestamp=Coalesce(Max('replies__submit_date'), 'created')).order_by(
            '-pinned',
            '-natural_timestamp')


class PostManager(models.Manager.from_queryset(PostQuerySet)):
    def get_queryset(self):
        return super().get_queryset().filter(is_removed=False, category__is_removed=False)


class Post(TimeStampedModel, SoftDeletableModel):
    title = models.CharField(_("title"), max_length=255)
    body = models.TextField(_("body"), blank=True)
    views = models.PositiveIntegerField(_("views"), default=0, editable=False)
    pinned = models.BooleanField(_("pinned"), default=False)
    highlighted = models.BooleanField(_("highlighted"), default=False)

    category = models.ForeignKey('categories.Category', verbose_name=_("category"))
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("author"))
    tags = TaggableManager(blank=True, verbose_name=_('tags'))
    replies = GenericRelation(Reply, object_id_field='object_pk', content_type_field='content_type',
                              verbose_name=_("replies"))

    objects = models.Manager()
    public = PostManager()

    class Meta:
        verbose_name = _('post')
        verbose_name_plural = _('posts')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('forum:detail', args=(self.pk,))

    def latest_reply(self):
        if self.replies.count():
            return self.replies.latest('submit_date')

    def timestamp(self):
        if self.latest_reply():
            return self.latest_reply().submit_date
        else:
            return self.created

    def get_replies(self):
        return self.replies.order_by('submit_date')

    def participants_count(self):
        return self.replies.values_list('user_id', flat=True).distinct().count()

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])
