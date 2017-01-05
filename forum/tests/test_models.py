import datetime

from django.test import TestCase
from django.utils import timezone
from django.contrib.sites.models import Site

from categories.models import Category
from users.models import User
from replies.models import Reply
from ..models import Post


class PostTestCase(TestCase):
    def test_manager_visible(self):
        user = User.objects.create_user(username='testuser', email='test@test.com', password='test8888')
        removed_category = Category.objects.create(name='removed', slug='removed', is_removed=True)
        visible_category = Category.objects.create(name='visible', slug='visible')
        Post.objects.create(
            title='visible post',
            category=visible_category,
            author=user
        )

        Post.objects.create(
            title='removed post',
            category=visible_category,
            author=user,
            is_removed=True
        )

        Post.objects.create(
            title='post in removed category',
            category=removed_category,
            author=user,
        )

        self.assertQuerysetEqual(Post.objects.visible(), ['<Post: visible post>'])

    def test_manager_ordered(self):
        now = timezone.now()
        user = User.objects.create_user(username='testuser', email='test@test.com', password='test8888')
        category = Category.objects.create(name='test category', slug='test-category')
        site = Site.objects.create(domain='test.com', name='example')

        post_1_minutes_ago = Post.objects.create(
            title='post has a reply created at 1 minutes ago',
            category=category,
            author=user,
            created=now - timezone.timedelta(minutes=30),
        )

        post_3_minutes_ago = Post.objects.create(
            title='post has a reply created at 3 minutes ago',
            category=category,
            author=user,
            created=now - timezone.timedelta(minutes=20),
        )

        Reply.objects.create(
            user=user,
            comment='test reply submit at 3 minutes ago',
            submit_date=now - timezone.timedelta(minutes=3),
            content_object=post_3_minutes_ago,
            site=site,
        )

        Reply.objects.create(
            user=user,
            comment='test reply submit at 1 minutes ago',
            submit_date=now - timezone.timedelta(minutes=1),
            content_object=post_1_minutes_ago,
            site=site,
        )

        Post.objects.create(
            title='post has no reply created at now',
            category=category,
            author=user,
            created=now
        )

        Post.objects.create(
            title='post has no reply created at 5 minutes ago',
            category=category,
            author=user,
            created=now - timezone.timedelta(minutes=5)
        )

        self.assertQuerysetEqual(Post.objects.ordered(), [
            '<Post: post has no reply created at now>',
            '<Post: post has a reply created at 1 minutes ago>',
            '<Post: post has a reply created at 3 minutes ago>',
            '<Post: post has no reply created at 5 minutes ago>',
        ])

    def test__str__(self):
        user = User.objects.create_user(username='testuser', email='test@test.com', password='test8888')
        category = Category.objects.create(name='test category', slug='test-category')
        post = Post.objects.create(
            title='test post',
            category=category,
            author=user,
        )
        self.assertEqual(post.__str__(), 'test post')

    def test_get_absolute_url(self):
        user = User.objects.create_user(username='testuser', email='test@test.com', password='test8888')
        category = Category.objects.create(name='test category', slug='test-category')
        post = Post.objects.create(
            title='test post',
            category=category,
            author=user,
        )
        self.assertEqual(post.__str__(), 'test post')
        self.assertRegex(post.get_absolute_url(), '/post/[0-9]+')

    def test_latest_reply(self):
        now = timezone.now()
        user = User.objects.create_user(username='testuser', email='test@test.com', password='test8888')
        category = Category.objects.create(name='test category', slug='test-category')
        site = Site.objects.create(domain='test.com', name='example')

        post = Post.objects.create(
            title='post has 2 reply',
            category=category,
            author=user,
            created=now - timezone.timedelta(minutes=30),
        )

        latest_reply = Reply.objects.create(
            user=user,
            comment='test reply submit at 3 minutes ago',
            submit_date=now - timezone.timedelta(minutes=5),
            content_object=post,
            site=site,
        )

        Reply.objects.create(
            user=user,
            comment='test reply submit at 1 minutes ago',
            submit_date=now - timezone.timedelta(minutes=10),
            content_object=post,
            site=site,
        )

        self.assertEqual(post.latest_reply(), latest_reply)

    def test_increase_views(self):
        user = User.objects.create_user(username='testuser', email='test@test.com', password='test8888')
        category = Category.objects.create(name='test category', slug='test-category')
        post = Post.objects.create(
            title='test post',
            category=category,
            author=user,
        )
        post.increase_views()
        self.assertEqual(post.views, 1)
