from django import forms
from django.core import urlresolvers
from django.contrib.auth.validators import UnicodeUsernameValidator

from allauth.account.forms import (
    LoginForm as AllAuthLoginForm,
    SignupForm as AllAuthSignupForm
)
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, HTML

from .models import User


class LoginForm(AllAuthLoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_action = 'account_login'
        self.helper.form_method = 'post'
        self.helper.layout.append(
            HTML("""
            <input type="hidden" name="{{ redirect_field_name }}"
            value="{% if redirect_field_value %}{{ redirect_field_value }}{% else %}/{% endif %}">'
            """))
        self.helper.add_input(Submit('submit', '登录'))


class SignupForm(AllAuthSignupForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_action = 'account_signup'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', '注册'))

        self.fields['username'].help_text = '用户名只能包含数字和字母'
        self.fields['password1'].help_text = '不能使用纯数字作为密码'


class UserProfileForm(forms.ModelForm):
    nickname = forms.CharField(validators=[UnicodeUsernameValidator(regex=r'^[\w_-]+$',
                                                                    message="除了下划线（_）和连字符（-）外，昵称中不能包含其他特殊符号"
                                                                    )])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.form_action = urlresolvers.reverse('users:profile_change')
        self.helper.add_input(Submit('submit', '确认修改'))

        self.fields['nickname'].label = '昵称'
        self.fields['nickname'].help_text = '除了下划线（_）和连字符（-）外，昵称中不能包含其它特殊符号'
        self.fields['signature'].label = '个性签名'

    class Meta:
        model = User
        fields = ('nickname', 'signature')

    def clean_nickname(self):
        nickname = self.cleaned_data['nickname']
        if len(nickname) > 10:
            raise forms.ValidationError("昵称长度不能超过10个字符")
        return nickname


class MugshotForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('mugshot',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.form_class = 'mt-1'
        self.helper.form_action = urlresolvers.reverse('users:mugshot_change')
        self.helper.add_input(Submit('submit', '开始上传'))
        self.fields['mugshot'].label = '头像'
