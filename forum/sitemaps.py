from django.contrib.sitemaps import GenericSitemap

from .models import Post
from categories.models import Category

post_info_dict = {
    'queryset': Post.objects.all(),
    'date_field': 'modified',
}

category_info_dict = {
    'queryset': Category.objects.all(),
}

sitemaps = {'post': GenericSitemap(post_info_dict, priority=0.5),
            'category': GenericSitemap(category_info_dict, priority=0.5)}
