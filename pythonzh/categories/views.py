from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from django.db.models import Max
from django.core.paginator import Paginator
from django.db.models.functions import Coalesce

from forum.models import Post
from forum.forms import PostCreationForm

from .models import Category


class CategoryPostView(ListView):
    paginate_orphans = 0
    paginate_by = 10
    template_name = 'categories/posts.html'

    def get_queryset(self):
        category = get_object_or_404(Category, slug=self.kwargs.get('slug'))
        return category.post_set.all().annotate(
            latest_reply_time=Coalesce(Max('replies__submit_date'), 'created')).order_by(
            '-pinned',
            '-latest_reply_time')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # TODO: duplicated query
        category = get_object_or_404(Category, slug=self.kwargs.get('slug'))
        category_ancestors = category.get_ancestors()
        form = PostCreationForm(initial={'category': category})

        context.update({
            'category': category,
            'category_ancestors': category_ancestors,
            'form': form
        })
        return context
