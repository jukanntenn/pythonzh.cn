import re

from django_comments.moderation import CommentModerator, Moderator as DjangoCommentModerator
from django.template.loader import render_to_string
from django.utils.html import mark_safe

from notifications.signals import notify

from users.models import User
from forum.mark import markdownify


class Moderator(DjangoCommentModerator):
    def post_save_moderation(self, sender, comment, request, **kwargs):
        model = comment.content_type.model_class()
        if model not in self._registry:
            return
        self._registry[model].reply(comment, comment.content_object, request)


class ReplyModerator(CommentModerator):
    def reply(self, reply, content_object, request):
        # 接受到评论会被 strip，不知道哪一步被处理的，临时为其补一个一个空格，防止@用户名在最后时无法解析
        reply.comment += ' '
        nicknames = re.findall(r'@(?P<nickname>[a-zA-Z0-9\u4e00-\u9fa5]+) ', reply.comment)
        users = User.objects.filter(nickname__in=nicknames)
        reply.comment = reply.comment.strip()

        if users:
            def mark(mo):
                nickname = mo.group(1)
                user = users.get(nickname=nickname)
                return '@[%s](%s)' % (nickname, user.get_absolute_url())

            pattern = '@(%s)' % ('|'.join(u.nickname for u in users))
            reply.comment = re.sub(pattern, mark, reply.comment)

            recipients = users.exclude(pk=reply.user.pk)

            for recipient in recipients:
                description = render_to_string('notifications/mention.html', {
                    'user': reply.user,
                    'post': content_object,
                    'reply': reply,
                    'content': markdownify(reply.comment)
                })
                data = {
                    'recipient': recipient,
                    'verb': '@',
                    'action_object': reply,
                    'target': recipient,
                    'description': description
                }
                notify.send(sender=reply.user, **data)

        if reply.user != content_object.author:
            description = render_to_string('notifications/reply.html', {
                'user': reply.user,
                'post': content_object,
                'reply': reply,
                'content': markdownify(reply.comment)
            })
            data = {
                'recipient': content_object.author,
                'verb': 'reply',
                'action_object': reply,
                'target': content_object.author,
                'description': description
            }

            notify.send(sender=reply.user, **data)

        reply.save()


moderator = Moderator()
