from django.views.generic import DetailView
from django.db.models import Max

from forum.models import Post
from .models import Category


class CategoryPostView(DetailView):
    model = Category
    template_name = 'categories/posts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post_list = Post.objects.filter(category__slug=self.kwargs.get('slug')).annotate(
            latest_reply_time=Max('replies__submit_date')).order_by('-pinned',
                                                                    '-latest_reply_time')
        context['post_list'] = post_list
        return context
