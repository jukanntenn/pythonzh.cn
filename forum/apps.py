from django.apps import AppConfig


class ForumConfig(AppConfig):
    name = 'forum'

    def ready(self):
        from replies.moderation import moderator
        from replies.moderation import ReplyModerator
        from replies.models import Reply
        from actstream import registry
        registry.register(Reply)
        registry.register(self.get_model('Post'))
        moderator.register(self.get_model('Post'), ReplyModerator)
