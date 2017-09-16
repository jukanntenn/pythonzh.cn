from django.core.exceptions import ValidationError
from django import forms

from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.models import EmailAddress
from allauth.account.utils import user_field

from users.models import User


class AccountAdapter(DefaultAccountAdapter):
    def __init__(self, request=None):
        super().__init__(request)
        self.error_messages['email_taken'] = "该邮箱已被注册。"
        self.error_messages['username_taken'] = "该用户名已被注册。"

    def save_user(self, request, user, form, commit=True):
        user = super().save_user(request, user, form, commit=False)
        user.ip_joined = request.META.get("REMOTE_ADDR", None)

        if commit:
            user.save()
        return user

    def clean_username(self, username, shallow=False):
        username = super().clean_username(username, shallow=False)
        if len(username) > 15:
            raise forms.ValidationError("用户名长度不能超过15个字符。")
        return username


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def is_auto_signup_allowed(self, request, sociallogin):
        return True

    def validate_disconnect(self, account, accounts):
        if len(accounts) == 1:
            if not account.user.has_usable_password():
                raise ValidationError("你的账户还没有设置密码。")

            if EmailAddress.objects.filter(user=account.user,
                                           verified=True).count() == 0:
                raise ValidationError("你的账户还没有已验证的邮箱。")
