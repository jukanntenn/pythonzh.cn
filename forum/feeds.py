from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from django.db.models.functions import Coalesce
from django.db.models import Max
from django.utils.feedgenerator import Atom1Feed

from .models import Post
from .utils import mark
from .templatetags.forum_tags import bleach_value


class AllPostsRssFeed(Feed):
    title = "django 测试论坛"
    link = "/"
    description = "首页的全部帖子"

    def items(self):
        return Post.objects.filter(is_removed=False).annotate(
            latest_reply_time=Coalesce(Max('replies__submit_date'), 'created')).order_by(
            '-pinned',
            '-latest_reply_time')

    def item_title(self, item):
        return '[%s] %s' % (item.category, item.title)

    def item_description(self, item):
        return bleach_value(mark(item.body))


class AllPostsAtomFeed(AllPostsRssFeed):
    feed_type = Atom1Feed
    subtitle = AllPostsRssFeed.description
