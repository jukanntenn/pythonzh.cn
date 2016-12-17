from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Max
from django.db.models.functions import Coalesce

from braces.views import UserFormKwargsMixin

from categories.models import Category
from .models import Post
from .forms import PostCreationForm


class IndexView(ListView):
    paginate_orphans = 5
    paginate_by = 10
    model = Post
    template_name = 'forum/index.html'

    def get_queryset(self):
        query = super().get_queryset().filter(is_removed=False).annotate(
            latest_reply_time=Coalesce(Max('replies__submit_date'), 'created')).order_by(
            '-pinned',
            '-latest_reply_time')

        return query


class PostDetailView(DetailView):
    model = Post
    template_name = 'forum/detail.html'


class PostCreateView(LoginRequiredMixin, UserFormKwargsMixin, CreateView):
    form_class = PostCreationForm
    template_name = 'forum/post_form.html'

    def get_initial(self):
        initial = super().get_initial()
        slug = self.kwargs.get('slug')
        if not slug:
            return initial
        category = get_object_or_404(Category, slug=slug)
        initial['category'] = category
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # TODO: duplicated query
        slug = self.kwargs.get('slug')
        if not slug:
            return context
        category = get_object_or_404(Category, slug=slug)
        context['category'] = category
        return context
