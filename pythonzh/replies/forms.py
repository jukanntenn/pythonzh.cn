from django import forms
from django.conf import settings

from django_comments.forms import CommentForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Hidden
from simplemde.widgets import SimpleMDEEditor
from pagedown.widgets import PagedownWidget

import django_comments

use_pagedown = getattr(settings, 'USE_PAGEDOWN')


class ReplyForm(CommentForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_action = django_comments.get_form_target()
        self.helper.form_id = 'id_reply_form'
        self.helper.attrs = {'novalidate': ''}
        # self.helper.include_media = False
        self.helper.layout = Layout(
            'honeypot',
            'content_type',
            'object_pk',
            'timestamp',
            'security_hash',
            'comment',
            Hidden('next', '{% url "replies:success" %}'),
        )
        self.helper.add_input(Submit('submit', '回复', css_class='btn-sm'))

        self.fields['comment'].label = ''

        if use_pagedown:
            self.fields['comment'].widget = PagedownWidget()
