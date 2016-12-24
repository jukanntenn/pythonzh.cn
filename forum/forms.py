from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from simplemde.widgets import SimpleMDEEditor

from .models import Post


class PostCreationForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'body', 'category',)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_action = 'forum:create'
        self.helper.form_method = 'post'
        self.helper.form_id = 'id_create_form'
        self.helper.add_input(Submit('submit', '发布'))
        self.helper.include_media = False
        # TODO: use Meta attribute
        self.fields['title'].label = '标题'
        self.fields['title'].help_text = '如果标题能够说明问题，可以不必填写正文'
        self.fields['body'].label = '正文'
        self.fields['body'].help_text = '支持 Markdown 语法标记'
        self.fields['category'].label = '分类'
        self.fields['category'].help_text = '选择帖子分类'
        self.fields['body'].widget = SimpleMDEEditor()

        if self.initial.get('category'):
            self.fields['category'].widget = forms.HiddenInput()

    def save(self, commit=True):
        if self.user:
            self.instance.author = self.user
        return super().save(commit=commit)


class PostEditForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'body', 'category',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', '发布'))
        self.helper.include_media = False
        # TODO: use Meta attribute
        self.fields['title'].label = '标题'
        self.fields['title'].help_text = '如果标题能够说明问题，可以不必填写正文'
        self.fields['body'].label = '正文'
        self.fields['body'].help_text = '支持 Markdown 语法标记'
        self.fields['category'].label = '分类'
        self.fields['category'].help_text = '选择帖子分类'
        self.fields['body'].widget = SimpleMDEEditor()
