from django import forms

from django_comments.forms import CommentForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Hidden

import django_comments


class ReplyForm(CommentForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_action = django_comments.get_form_target()
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
