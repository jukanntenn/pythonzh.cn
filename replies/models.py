from django.db import models
from django.utils.translation import ugettext_lazy as _

from django_comments.abstracts import CommentAbstractModel
from django_comments.managers import CommentManager
from mptt.models import MPTTModel
from mptt.models import MPTTModel, TreeForeignKey
from mptt.managers import TreeManager

from forum.utils import markdown_value
from forum.utils import parse_nicknames


class ReplyManager(TreeManager, CommentManager):
    pass


class Reply(MPTTModel, CommentAbstractModel):
    parent = TreeForeignKey('self', null=True, blank=True,
                            verbose_name=_('parent reply'), related_name='children',
                            on_delete=models.SET_NULL)
    objects = ReplyManager()

    class Meta(CommentAbstractModel.Meta):
        verbose_name = _('reply')
        verbose_name_plural = _('replies')

    @property
    def reply_html(self):
        return markdown_value(parse_nicknames(self.comment))
