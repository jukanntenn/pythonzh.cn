from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'users'

    def ready(self):
        from allauth.account.signals import user_logged_in, user_signed_up
        from .receivers import update_joined, update_last_login

        user_signed_up.connect(update_joined)
        user_logged_in.connect(update_last_login)
