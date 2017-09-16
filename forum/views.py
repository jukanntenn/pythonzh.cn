from django.http import HttpResponseForbidden, JsonResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, View, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Max
from django.db.models.functions import Coalesce
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.views.decorators.csrf import csrf_exempt

from actstream import actions
from actstream.views import respond
from actstream.compat import get_model
from actstream.signals import action
from actstream.registry import check
from notifications.views import AllNotificationsList
from braces.views import UserFormKwargsMixin
from notifications.signals import notify

from categories.models import Category
from .models import Post
from .forms import PostCreationForm, PostEditForm
from .utils import markdown_value, bleach_value, parse_nicknames
from .mixins import PaginationMixin


class AboutView(TemplateView):
    template_name = 'forum/about.html'


class ContactView(TemplateView):
    template_name = 'forum/contact.html'


class DonateView(TemplateView):
    template_name = 'forum/donate.html'


class ContentPreviewView(View):
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        raw_content = self.request.POST.get('content')
        preview_content = ''
        if raw_content:
            preview_content = parse_nicknames(markdown_value(bleach_value(raw_content)))

        return JsonResponse({'preview': preview_content})


class IndexView(PaginationMixin, ListView):
    paginate_orphans = 5
    paginate_by = 20
    model = Post
    template_name = 'forum/index.html'

    def get_queryset(self):
        return Post.public.all().natural_order()


class PostDetailView(DetailView):
    model = Post
    template_name = 'forum/detail.html'

    def get(self, request, *args, **kwargs):
        response = super(PostDetailView, self).get(request, *args, **kwargs)
        self.object.increase_views()
        return response

    def get_queryset(self):
        return Post.public.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ctype = ContentType.objects.get_for_model(self.object)
        context['ctype'] = ctype
        return context


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
    template_name = 'forum/post_edit_form.html'

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)

        # TODO: use a more elegent way
        if self.request.user != self.object.author and not request.user.is_superuser:
            return HttpResponseForbidden('只有帖子的作者才能编辑该帖子')
        return response

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if self.request.user != self.object.author and not request.user.is_superuser:
            return HttpResponseForbidden('只有帖子的作者才能编辑该帖子')
        return response

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        return form

    def form_valid(self, form):
        response = super().form_valid(form)
        return response


class NotificationsListView(PaginationMixin, AllNotificationsList):
    paginate_by = 20
    paginate_orphans = 5


class CategoryPostListView(PaginationMixin, ListView):
    paginate_orphans = 5
    paginate_by = 20
    template_name = 'forum/category_post_list.html'

    def get(self, request, *args, **kwargs):
        slug = self.kwargs.get('slug')
        self.category = get_object_or_404(Category, slug=slug, is_removed=False)
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        cates = self.category.get_descendants(include_self=True)
        return Post.public.filter(category__in=cates).natural_order()

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

    def get_template_names(self):
        names = super().get_template_names()

        if not self.category.parent:
            names.insert(0, 'forum/index.html')

        return names


RECIPIENT = {
    'Post': 'author',
    'Reply': 'user',
}


def follow(user, obj, send_action=True, actor_only=True, **kwargs):
    check(obj)
    follow_type = kwargs.pop('follow_type', '')
    instance, created = get_model('actstream', 'follow').objects.get_or_create(
        user=user, object_id=obj.pk, follow_type=follow_type,
        content_type=ContentType.objects.get_for_model(obj),
        actor_only=actor_only)
    if send_action and created:
        if not follow_type:
            action.send(user, verb=_('started following'), target=obj, **kwargs)
        else:
            action.send(user, verb=_('started %s' % follow_type), target=obj, **kwargs)

    if obj.__class__.__name__ not in RECIPIENT:
        recipient = obj
    else:
        recipient = getattr(obj, RECIPIENT[obj.__class__.__name__], None)

    if created and recipient and user != recipient:
        if follow_type and not follow_type.startswith('un'):
            notify.send(sender=user, recipient=recipient, verb=follow_type, target=obj)
    return instance


@login_required
@csrf_exempt
def follow_unfollow(request, content_type_id, object_id, do_follow=True, actor_only=True, send_action=True,
                    follow_type=None):
    ctype = get_object_or_404(ContentType, pk=content_type_id)
    instance = get_object_or_404(ctype.model_class(), pk=object_id)

    if do_follow:
        if not follow_type:
            follow(request.user, instance, actor_only=actor_only, send_action=send_action)
        else:
            follow(request.user, instance, actor_only=actor_only, send_action=send_action,
                   follow_type=follow_type)
        return respond(request, 201)  # CREATED
    actions.unfollow(request.user, instance, follow_type=follow_type)
    return respond(request, 204)  # NO CONTENT
