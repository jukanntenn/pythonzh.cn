from django.shortcuts import render, get_object_or_404
from django.views.generic import View, DetailView, RedirectView

from .models import Reply


class ReplySuccess(RedirectView):
    permanent = True

    def get_redirect_url(self, *args, **kwargs):
        self.url = self.reply.get_absolute_url()
        return super().get_redirect_url(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.reply = get_object_or_404(Reply, pk=request.GET.get('c'))
        return super().get(request, *args, **kwargs)
