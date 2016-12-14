from django.utils.translation import ugettext_lazy as _

from django_comments.abstracts import CommentAbstractModel


class Reply(CommentAbstractModel):
    class Meta(CommentAbstractModel.Meta):
        verbose_name = _('reply')
        verbose_name_plural = _('replies')
