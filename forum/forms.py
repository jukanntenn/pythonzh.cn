from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .models import Post


class PostCreationForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'body', 'category',)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_action = 'forum:create'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', '发布'))

    def save(self, commit=True):
        self.instance.author = self.user
        return super().save(commit=commit)
