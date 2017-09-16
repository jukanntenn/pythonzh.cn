from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from model_utils.models import TimeStampedModel, SoftDeletableModel, SoftDeletableManager
from mptt.models import MPTTModel, TreeForeignKey
from mptt.managers import TreeManager


class CategoryManager(TreeManager, SoftDeletableManager):
    """
    将来可能的拓展
    """
    pass


class Category(MPTTModel, TimeStampedModel, SoftDeletableModel):
    """
    来自父类的 fields：

    created - 自动记录创建时间
    modified - 自动记录更新时间
    is_removed
    """
    parent = TreeForeignKey('self', null=True, blank=True, verbose_name=_("parent category"),
                            related_name='children', on_delete=models.SET_NULL)
    name = models.CharField(_("name"), max_length=255, unique=True)
    cover = models.OneToOneField('covers.Cover', blank=True, null=True, verbose_name=_("cover"),
                                 on_delete=models.SET_NULL)
    slug = models.SlugField(_("slug"), max_length=255, unique=True, allow_unicode=True)
    description = models.TextField(_("description"), blank=True)
    rank = models.PositiveIntegerField(_("rank"), null=True, blank=True,
                                       help_text=_("determine the display order on index page."))
    show = models.BooleanField(_("show"), default=False,
                               help_text=_("determine whether display on index page or not."))

    objects = TreeManager()
    public = CategoryManager()

    class Meta:
        verbose_name = _("category")
        verbose_name_plural = _("categories")

    class MPTTMeta:
        order_insertion_by = ['-created']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('forum:category_posts', kwargs={'slug': self.slug})
