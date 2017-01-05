from django.utils.translation import ugettext_lazy as _

from django_comments.abstracts import CommentAbstractModel

from forum.utils import mark
from forum.utils import parse_nicknames


class Reply(CommentAbstractModel):
    class Meta(CommentAbstractModel.Meta):
        verbose_name = _('reply')
        verbose_name_plural = _('replies')

    @property
    def reply_html(self):
        return mark(parse_nicknames(self.comment))
