from django.db import models
from django.utils.translation import ugettext_lazy as _

from model_utils.models import TimeStampedModel, SoftDeletableModel, SoftDeletableManager
from mptt.models import MPTTModel, TreeForeignKey
from mptt.managers import TreeManager


class CategoryManager(TreeManager, SoftDeletableManager):
    pass


class Category(MPTTModel, TimeStampedModel, SoftDeletableModel):
    parent = TreeForeignKey('self', null=True, blank=True,
                            verbose_name=_('parent category'), related_name='children',
                            on_delete=models.SET_NULL)
    name = models.CharField(_('name'), max_length=255, unique=True)
    cover = models.OneToOneField('covers.Cover', verbose_name=_('cover'), blank=True, null=True,
                                 on_delete=models.SET_NULL)
    slug = models.SlugField(_('slug'), max_length=255, unique=True, allow_unicode=True)
    description = models.TextField(_('description'), blank=True)

    objects = TreeManager()
    public = CategoryManager()

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')

    class MPTTMeta:
        order_insertion_by = ['-created']

    def __str__(self):
        return self.name
