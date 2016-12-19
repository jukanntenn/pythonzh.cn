import re

from django.core.exceptions import ValidationError

from allauth.account.adapter import DefaultAccountAdapter


class AccountAdapter(DefaultAccountAdapter):
    username_regex = re.compile(r'^[0-9A-Za-z]+$')

    def clean_username(self, username, *args, **kwargs):
        self.error_messages['invalid_username'] = "用户名只能包含数字和字母"
        if len(username) > 10:
            raise ValidationError("用户名最长为10个字符")
        return super().clean_username(username, *args, **kwargs)
