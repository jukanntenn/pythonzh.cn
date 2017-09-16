import re

from django_comments.moderation import CommentModerator, Moderator as DjangoCommentModerator

from notifications.signals import notify

from users.models import User


class Moderator(DjangoCommentModerator):
    def post_save_moderation(self, sender, comment, request, **kwargs):
        model = comment.content_type.model_class()
        if model not in self._registry:
            return
        self._registry[model].reply(comment, comment.content_object, request)


class ReplyModerator(CommentModerator):
    def reply(self, reply, content_object, request):

        # 接受到评论会被 strip，不知道哪一步被处理的，临时为其补一个空格，防止@用户名在最后时无法解析
        reply.comment += ' '
        nicknames = re.findall(r'@(?P<nickname>.+?) ', reply.comment)
        users = User.objects.filter(nickname__in=nicknames)
        reply.comment = reply.comment.strip()

        mentioned = False
        if users:
            def mark(mo):
                nickname = mo.group(1)
                user = users.get(nickname=nickname)
                return '@[%d](%s)' % (user.pk, user.get_absolute_url())

            pattern = '@(%s)' % ('|'.join(u.nickname for u in users))
            reply.comment = re.sub(pattern, mark, reply.comment)

            # 自己 @ 自己不会收到通知
            recipients = users.exclude(pk=reply.user.pk)

            if content_object.author in recipients:
                mentioned = True

            for recipient in recipients:
                data = {
                    'recipient': recipient,
                    'verb': '@',
                    'target': reply,
                }
                notify.send(sender=reply.user, **data)

        # 如果帖子作者没被 @ 并且回复者不是作者自己，则向作者发送一条通知
        if not mentioned and reply.user != content_object.author:
            data = {
                'recipient': content_object.author,
                'verb': 'reply',
                'target': reply,
            }

            notify.send(sender=reply.user, **data)

        reply.save()


moderator = Moderator()
