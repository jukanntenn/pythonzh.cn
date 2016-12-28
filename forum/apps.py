from django.apps import AppConfig


class ForumConfig(AppConfig):
    name = 'forum'

    def ready(self):
        from replies.moderation import moderator
        from replies.moderation import ReplyModerator
        from actstream import registry
        moderator.register(self.get_model('Post'), ReplyModerator)
        registry.register(self.get_model('Post'))
