from django import template
from django.db.models import Count

from categories.models import Category
from ..models import Post

register = template.Library()


@register.simple_tag
def get_popular_posts():
    return Post.objects.all().annotate(num_replies=Count('replies')).order_by('-num_replies')[:6]


@register.simple_tag
def get_categories():
    return Category.objects.filter(parent__isnull=True)


@register.simple_tag
def get_quick_categories():
    return Category.objects.filter(parent__isnull=False)
