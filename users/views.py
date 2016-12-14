from django.shortcuts import render
from django.views.generic import TemplateView, UpdateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse

from .forms import UserProfileForm, MugshotForm
from .models import User


class UserProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'users/profile.html'


class UserProfileChangeView(LoginRequiredMixin, UpdateView):
    slug_field = 'username'
    slug_url_kwarg = 'username'
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile_change.html'
    success_url = '/accounts/profile'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.helper.form_action = reverse('users:profile_change', args=(self.object.username,))
        return form


class MugshotChangeView(LoginRequiredMixin, UpdateView):
    slug_field = 'username'
    slug_url_kwarg = 'username'
    model = User
    form_class = MugshotForm
    template_name = 'users/mugshot_change.html'
    success_url = '/accounts/profile'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.helper.form_action = reverse('users:mugshot_change', args=(self.object.username,))
        return form

    def form_valid(self, form):
        if form.has_changed():
            self.request.user.mugshot.delete(save=False)
        return super().form_valid(form)


class UserDetailView(DetailView):
    model = User
    slug_field = 'username'
    slug_url_kwarg = 'username'
    template_name = 'users/detail.html'
