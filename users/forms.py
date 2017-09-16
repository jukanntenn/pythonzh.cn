from django import forms
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.template.defaultfilters import filesizeformat

from allauth.account.forms import (
    LoginForm as AllAuthLoginForm,
    SignupForm as AllAuthSignupForm,
    ResetPasswordForm as AllAuthResetPasswordForm,
    AddEmailForm as AllAuthAddEmailForm,
)

from captcha.fields import CaptchaField

from .models import User


class LoginForm(AllAuthLoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['remember'].label_suffix = ''


class SignupForm(AllAuthSignupForm):
    captcha = CaptchaField(label='验证码')


class ResetPasswordForm(AllAuthResetPasswordForm):
    captcha = CaptchaField(label='验证码')


class AddEmailForm(AllAuthAddEmailForm):
    captcha = CaptchaField(label='验证码')


class UserProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nickname'].validators.append(UnicodeUsernameValidator(message='昵称中含有非法字符。'))
        self.fields['nickname'].label = '昵称'
        self.fields['signature'].label = '个性签名'
        self.fields['mugshot'].label = '头像'

    class Meta:
        model = User
        fields = ('nickname', 'signature', 'mugshot')

    def clean_nickname(self):
        nickname = self.cleaned_data['nickname']
        if len(nickname) > 15:
            raise forms.ValidationError("昵称长度不能超过15个字符。")
        return nickname

    def clean_mugshot(self):
        content = self.cleaned_data.get('mugshot')
        if content.size > 1024 * 1024:
            raise forms.ValidationError('上传的图片大小不能超过 %s。' % filesizeformat(1024 * 1024))
        return content
