from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, UpdateView, DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse
from django.db.models import Q

from actstream.models import actor_stream, Action

from follows.models import Follow
from forum.models import Post
from replies.models import Reply
from .forms import UserProfileForm, MugshotForm
from .models import User


class UserProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'users/profile.html'


class UserProfileChangeView(LoginRequiredMixin, UpdateView):
    form_class = UserProfileForm
    template_name = 'users/profile_change.html'
    success_url = '/users/profile'

    def get_object(self, queryset=None):
        return self.request.user


class MugshotChangeView(LoginRequiredMixin, UpdateView):
    form_class = MugshotForm
    template_name = 'users/mugshot_change.html'
    success_url = '/users/profile'

    def form_valid(self, form):
        if form.has_changed():
            self.request.user.mugshot.delete(save=False)
        return super().form_valid(form)

    def get_object(self, queryset=None):
        return User.objects.get(pk=self.request.user.pk)


class UserDetailView(DetailView):
    model = User
    slug_field = 'username'
    slug_url_kwarg = 'username'
    template_name = 'users/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts = self.object.post_set.all().order_by('-created')[:10]
        replies = self.object.reply_comments.all().order_by('-submit_date')[:10]

        actions = actor_stream(self.object)[:20]

        context.update({
            'post_list': posts,
            'reply_list': replies,
            'action_list': actions,
        })
        return context


class UserActionView(ListView):
    paginate_by = 30
    model = Action
    template_name = 'users/actions.html'

    def get_queryset(self):
        return actor_stream(get_object_or_404(User, username=self.kwargs.get('username')))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username=self.kwargs.get('username'))
        context['user'] = user
        return context


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


class UserFavoriteView(LoginRequiredMixin, ListView):
    paginate_by = 10
    context_object_name = 'favorite_list'
    template_name = 'users/favorite_posts.html'

    def get_queryset(self):
        return self.request.user.follows.filter(ftype='favorite').order_by('-started')


class UserLikeView(ListView):
    model = Follow
    paginate_by = 20
    context_object_name = 'like_list'
    template_name = 'users/likes.html'

    def get_queryset(self):
        return super().get_queryset().filter(Q(ftype='watch') | Q(ftype='praise'),
                                             user__username=self.kwargs.get('username')
                                             ).order_by('-started')


class UserFeedView(LoginRequiredMixin, ListView):
    model = Action
    paginate_by = 10
    context_object_name = 'feed_list'
    template_name = 'users/feeds.html'

    # TODO: 只显示用户订阅后的动态，订阅前不显示
    def get_queryset(self):
        user_watch = [follow for follow in self.request.user.follows.filter(ftype='watch')]
        user_follow = [follow for follow in self.request.user.follows.filter(ftype='follow')]

        user_watch_id = [follow.follow_object.pk for follow in user_watch]
        user_follow_id = [follow.follow_object.pk for follow in user_follow]

        return super().get_queryset().filter(
            Q(actor_object_id__in=user_follow_id) | Q(action_object_object_id__in=user_watch_id,
                                                      verb='reply') | Q(target_object_id__in=user_watch_id,
                                                                        verb='edit')).order_by(
            '-timestamp')
