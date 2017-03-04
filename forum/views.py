from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Max
from django.db.models.functions import Coalesce
from django.core import urlresolvers
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType

from notifications.views import AllNotificationsList
from braces.views import UserFormKwargsMixin
from actstream.signals import action

from categories.models import Category
from .models import Post
from .forms import PostCreationForm, PostEditForm


class IndexView(ListView):
    paginate_orphans = 5
    paginate_by = 25
    model = Post
    template_name = 'forum/index.html'

    def get_queryset(self):
        query = super().get_queryset().all()
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

    def dispatch(self, request, *args, **kwargs):
        slug = self.kwargs.get('slug')
        self.category = None

        if slug:
            self.category = get_object_or_404(Category, slug=slug, is_removed=False)

        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        initial = super().get_initial()

        if not self.category:
            return initial

        initial['category'] = self.category
        return initial

    def post(self, request, *args, **kwargs):
        # TODO：add rate limit
        try:
            latest_post = self.request.user.post_set.latest('created')
            if latest_post.created + timezone.timedelta(seconds=5) > timezone.now():
                return HttpResponseForbidden('您的发帖时间间隔小于 5 秒钟，请稍微休息一会')
        except Post.DoesNotExist:
            pass

        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        action.send(self.request.user, verb='post', target=self.object)
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if not self.category:
            return context

        context['category'] = self.category
        return context


class PostEditView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostEditForm
    template_name = 'forum/post_form.html'

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)

        # TODO: use a more elegent way
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

    def form_valid(self, form):
        response = super().form_valid(form)
        action.send(self.request.user, verb='edit', target=self.object)
        return response


class NotificationsListView(AllNotificationsList):
    paginate_by = 10


class CategoryPostListView(ListView):
    paginate_orphans = 0
    paginate_by = 25
    template_name = 'forum/category_post_list.html'

    def get(self, request, *args, **kwargs):
        slug = self.kwargs.get('slug')
        self.category = get_object_or_404(Category, slug=slug, is_removed=False)
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return self.category.post_set.all().annotate(
            latest_reply_time=Coalesce(Max('replies__submit_date'), 'created')).order_by(
            '-pinned',
            '-latest_reply_time')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ancestors = self.category.get_ancestors()
        children = self.category.children.all()
        form = PostCreationForm(initial={'category': self.category})

        context.update({
            'category': self.category,
            'category_ancestors': ancestors,
            'category_children': children,
            'form': form
        })
        return context
