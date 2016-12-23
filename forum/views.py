from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Max
from django.db.models.functions import Coalesce
from django.core import urlresolvers
from django.utils import timezone

from notifications.views import AllNotificationsList

from braces.views import UserFormKwargsMixin

from categories.models import Category
from .models import Post
from .forms import PostCreationForm, PostEditForm


class IndexView(ListView):
    paginate_orphans = 5
    paginate_by = 20
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

    def get(self, request, *args, **kwargs):
        response = super(PostDetailView, self).get(request, *args, **kwargs)
        self.object.increase_views()
        return response


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

    def post(self, request, *args, **kwargs):
        try:
            latest_post = self.request.user.post_set.all().latest('created')
            if latest_post.created + timezone.timedelta(minutes=5) > timezone.now():
                return HttpResponseForbidden('您的发帖时间间隔小于 5 分钟，请稍微休息一会')
        except Post.DoesNotExist:
            pass

        return super().post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # TODO: duplicated query
        slug = self.kwargs.get('slug')
        if not slug:
            return context
        category = get_object_or_404(Category, slug=slug)
        context['category'] = category
        return context


class PostEditView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostEditForm
    template_name = 'forum/post_form.html'

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        if self.request.user != self.object.author:
            return HttpResponseForbidden('只有帖子的作者才能编辑该帖子')
        return response

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if self.request.user != self.object.author:
            return HttpResponseForbidden('只有帖子的作者才能编辑该帖子')
        return response

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.helper.form_action = urlresolvers.reverse('forum:edit', kwargs={'pk': self.kwargs.get('pk')})
        return form


class NotificationsListView(AllNotificationsList):
    paginate_by = 10
