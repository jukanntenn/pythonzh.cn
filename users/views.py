from django.views.generic import UpdateView, DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from braces.views import FormValidMessageMixin
from actstream.models import Follow

from forum.models import Post
from replies.models import Reply
from .forms import UserProfileForm
from .models import User


class UserProfileView(LoginRequiredMixin, FormValidMessageMixin, UpdateView):
    template_name = 'users/profile.html'
    form_class = UserProfileForm
    success_url = reverse_lazy('users:settings')
    form_valid_message = "个人资料更新成功！"
    context_object_name = 'forum_user'

    def get_object(self, queryset=None):
        return User.objects.get(pk=self.request.user.pk)

    def form_valid(self, form):
        if 'mugshot' in form.changed_data:
            self.request.user.mugshot.delete(save=False)
        return super().form_valid(form)


class UserDetailView(DetailView):
    model = User
    slug_field = 'username'
    slug_url_kwarg = 'username'
    template_name = 'users/detail.html'
    context_object_name = 'forum_user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts = self.object.post_set.all().order_by('-created')
        replies = self.object.reply_comments.all().order_by('-submit_date')
        favorite_post_list = Follow.objects.following_qs(self.object, follow_type='favorite')
        context.update({
            'post_list': posts,
            'reply_list': replies,
            'favorite_post_list': favorite_post_list,
        })
        return context


"""
class UserPostListView(ListView):
    paginate_by = 10
    model = Post
    template_name = 'users/user_posts.html'

    def get_queryset(self):
        return super().get_queryset().filter(author__username=self.kwargs.get('username')).order_by('-created')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username=self.kwargs.get('username'))
        context['user'] = user
        return context


class UserReplyListView(ListView):
    paginate_by = 10
    model = Reply
    template_name = 'users/user_replies.html'

    def get_queryset(self):
        return super().get_queryset().filter(user__username=self.kwargs.get('username')).order_by('-submit_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username=self.kwargs.get('username'))
        context['user'] = user
        return context
"""
