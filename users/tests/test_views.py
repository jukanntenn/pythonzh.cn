from django.test import TestCase
from django.contrib.sites.models import Site
from django.urls import reverse

from ..models import User
from categories.models import Category
from forum.models import Post
from replies.models import Reply
from actstream.models import Follow


# TODO: test mugshot
class UserProfileViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@test.com', password='test8888')

    def test_use_correct_template(self):
        self.client.login(username='testuser', password='test8888')
        response = self.client.get(reverse('users:settings'))
        self.assertTemplateUsed(response, 'users/profile.html')


class UserDetailViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@test.com', password='test8888')

    def test_use_correct_template(self):
        self.client.login(username='testuser', password='test8888')
        response = self.client.get(reverse('users:detail', args=(self.user.pk,)))
        self.assertTemplateUsed(response, 'users/detail.html')

    def test_get_context_data(self):
        site = Site.objects.create(domain='test.com', name='example')
        category = Category.objects.create(name='test category', slug='test-category')
        post1 = Post.objects.create(title='test post1', category=category, author=self.user)
        post2 = Post.objects.create(title='test post2', category=category, author=self.user)
        reply1 = Reply.objects.create(user=self.user, comment='reply for post1', content_object=post1, site=site)
        reply2 = Reply.objects.create(user=self.user, comment='reply for post2', content_object=post2, site=site)
        follow1 = Follow.objects.create(user=self.user, follow_object=post1, follow_type='favorite')
        follow2 = Follow.objects.create(user=self.user, follow_object=post2, follow_type='favorite')

        self.client.login(username='testuser', password='test8888')
        response = self.client.get(reverse('users:detail', args=(self.user.pk,)))

        self.assertEqual(response.context['post_list'].count(), 2)
        self.assertQuerysetEqual(response.context['post_list'], ['<Post: test post1>', '<Post: test post2>'])

        self.assertEqual(response.context['reply_list'].count(), 2)
        self.assertQuerysetEqual(response.context['reply_list'], [repr(reply1), repr(reply2)])

        self.assertEqual(response.context['favorite_post_list'].count(), 2)
        self.assertQuerysetEqual(response.context['favorite_post_list'].order_by('-started'),
                                 [repr(follow1), repr(follow2)])
