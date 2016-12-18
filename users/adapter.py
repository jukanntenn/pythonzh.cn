import re

from allauth.account.adapter import DefaultAccountAdapter


class AccountAdapter(DefaultAccountAdapter):
    username_regex = re.compile(r'^[\w]+$')

    def clean_username(self, *args, **kwargs):
        self.error_messages['invalid_username'] = "用户名只能包含数字和字母"
        return super().clean_username(*args, **kwargs)
