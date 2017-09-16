from django import forms
from django_comments.forms import CommentForm

from . import get_model


class ReplyForm(CommentForm):
    parent = forms.IntegerField(required=False, widget=forms.HiddenInput)

    def __init__(self, target_object, parent=None, data=None, initial=None, **kwargs):
        self.parent = parent
        if initial is None:
            initial = {}
        initial.update({'parent': self.parent})
        super().__init__(target_object, data=data, initial=initial, **kwargs)
        self.fields['comment'].label = ''

    def get_comment_model(self):
        return get_model()

    def get_comment_create_data(self, **kwargs):
        d = super().get_comment_create_data()
        d['parent_id'] = self.cleaned_data['parent']
        return d
