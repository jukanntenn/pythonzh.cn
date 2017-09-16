import datetime

from django.test import TestCase
from django.utils import timezone
from django.contrib.sites.models import Site

from categories.models import Category
from users.models import User
from replies.models import Reply
from ..models import Post


def set_created_time(minutes=0):
    return timezone.now() - timezone.timedelta(minutes=minutes)


class PostQuerySetTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user', email='user@test.com', password='test8888')
        self.category = Category.objects.create(name='category', slug='category')
        self.site = Site.objects.create(domain='test.com', name='example')

    def test_natural_order(self):
        # 发布 4 篇帖子，1 篇置顶
        self.pinned_post = Post.objects.create(title='pinned post', category=self.category, author=self.user,
                                               pinned=True, created=set_created_time(minutes=100))
        self.post1 = Post.objects.create(title='post 1', category=self.category, author=self.user,
                                         created=set_created_time(minutes=3))
        self.post2 = Post.objects.create(title='post 2', category=self.category, author=self.user,
                                         created=set_created_time(minutes=2))
        self.post3 = Post.objects.create(title='post 3', category=self.category, author=self.user,
                                         created=set_created_time(minutes=1))

        # 最后发表的排前面，置顶帖始终排最前
        self.assertQuerysetEqual(Post.public.all().natural_order(),
                                 ['<Post: pinned post>',
                                  '<Post: post 3>',
                                  '<Post: post 2>',
                                  '<Post: post 1>'])

        # post2 被回复，此时 post2 排更前
        Reply.objects.create(user=self.user, comment='reply for post2', content_object=self.post2,
                             site=self.site)
        self.assertQuerysetEqual(Post.public.all().natural_order(),
                                 ['<Post: pinned post>',
                                  '<Post: post 2>',
                                  '<Post: post 3>',
                                  '<Post: post 1>'])

        # post1 被回复，此时 post1 排更前
        Reply.objects.create(user=self.user, comment='reply for post1', content_object=self.post1,
                             site=self.site)
        self.assertQuerysetEqual(Post.public.all().natural_order(),
                                 ['<Post: pinned post>',
                                  '<Post: post 1>',
                                  '<Post: post 2>',
                                  '<Post: post 3>'])


class PostManagerTestCase(TestCase):
    def setUp(self):
        """
        post1: visible category
        post2: removed category
        post3: removed post
        """
        self.user = User.objects.create_user(username='user', email='user@test.com', password='test8888')
        self.removed_category = Category.objects.create(name='removed', slug='removed', is_removed=True)
        self.visible_category = Category.objects.create(name='visible', slug='visible')

        Post.objects.create(title='visible post1', category=self.visible_category, author=self.user)
        Post.objects.create(title='visible post2 in removed category', category=self.removed_category,
                            author=self.user)
        Post.objects.create(title='removed post3', category=self.removed_category, author=self.user)

    def test_get_queryset(self):
        self.assertQuerysetEqual(Post.public.all(), ['<Post: visible post1>', ])
        self.assertEqual(Post.objects.all().count(), 3)


class PostTestCase(TestCase):
    def setUp(self):
        """
        """
        self.user1 = User.objects.create_user(username='user1', email='user1@test.com', password='test8888')
        self.user2 = User.objects.create_user(username='user2', email='user2@test.com', password='test8888')
        self.user3 = User.objects.create_user(username='user3', email='user3@test.com', password='test8888')
        self.category = Category.objects.create(name='category', slug='category')
        self.site = Site.objects.create(domain='test.com', name='example')
        self.post = Post.objects.create(title='post', category=self.category, author=self.user1)

    def test_str(self):
        self.assertEqual(str(self.post), 'post')

    def test_get_absolute_url(self):
        self.assertEqual(self.post.get_absolute_url(), '/post/%s/' % self.post.pk)

    def test_latest_reply(self):
        # 没有回复
        self.assertIs(self.post.latest_reply(), None)

        # 有回复
        latest_reply = Reply.objects.create(user=self.user1, comment='reply submit at 5 minutes ago', site=self.site,
                                            submit_date=set_created_time(minutes=5), content_object=self.post)
        self.assertEqual(self.post.latest_reply(), latest_reply)

        # 有更新的回复
        latest_reply = Reply.objects.create(user=self.user1, comment='reply submit at 1 minutes ago', site=self.site,
                                            submit_date=set_created_time(minutes=1), content_object=self.post)
        self.assertEqual(self.post.latest_reply(), latest_reply)

    def test_timestamp(self):
        self.assertEqual(self.post.timestamp(), self.post.created)

        # 有回复
        latest_reply = Reply.objects.create(user=self.user1, comment='reply submit at 5 minutes ago', site=self.site,
                                            submit_date=set_created_time(minutes=5), content_object=self.post)
        self.assertEqual(self.post.timestamp(), latest_reply.submit_date)

    def test_get_replies(self):
        reply1 = Reply.objects.create(user=self.user1, comment='reply1 at 5 minutes ago',
                                      submit_date=set_created_time(minutes=5),
                                      content_object=self.post, site=self.site)

        reply2 = Reply.objects.create(user=self.user1, comment='reply1 at 1 minutes ago',
                                      submit_date=set_created_time(minutes=1), content_object=self.post,
                                      site=self.site)

        self.assertQuerysetEqual(self.post.get_replies(), ['<Reply: %s>' % str(reply1), '<Reply: %s>' % str(reply2)])

    def test_participants_count(self):
        self.assertEqual(self.post.participants_count(), 0)

        Reply.objects.create(
            user=self.user1,
            comment='reply submit at 5 minutes ago',
            submit_date=set_created_time(minutes=5),
            content_object=self.post,
            site=self.site,
        )
        self.assertEqual(self.post.participants_count(), 1)

        Reply.objects.create(
            user=self.user2,
            comment='reply submit at 2 minutes ago',
            submit_date=set_created_time(minutes=2),
            content_object=self.post,
            site=self.site,
        )
        self.assertEqual(self.post.participants_count(), 2)

        Reply.objects.create(
            user=self.user3,
            comment='reply submit at 1 minutes ago',
            submit_date=set_created_time(minutes=1),
            content_object=self.post,
            site=self.site,
        )
        self.assertEqual(self.post.participants_count(), 3)

        Reply.objects.create(
            user=self.user2,
            comment='reply submit at by user2',
            submit_date=set_created_time(),
            content_object=self.post,
            site=self.site,
        )
        self.assertEqual(self.post.participants_count(), 3)

    def test_increase_views(self):
        self.post.increase_views()
        self.assertEqual(self.post.views, 1)

        self.post.increase_views()
        self.assertEqual(self.post.views, 2)
