from django import forms
from django.core import urlresolvers

from allauth.account.forms import (
    LoginForm as AllAuthLoginForm,
    SignupForm as AllAuthSignupForm
)
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .models import User


class LoginForm(AllAuthLoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_action = 'account_login'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', '登录'))


class SignupForm(AllAuthSignupForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_action = 'account_signup'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', '注册'))


class UserProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.form_action = urlresolvers.reverse('users:profile_change')
        self.helper.add_input(Submit('submit', '确认修改'))

    class Meta:
        model = User
        fields = ('nickname', 'signature')


class MugshotForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('mugshot',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.form_action = urlresolvers.reverse('users:mugshot_change')
        self.helper.add_input(Submit('submit', '开始上传'))
