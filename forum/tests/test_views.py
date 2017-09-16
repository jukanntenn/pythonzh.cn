import json

from django.test import TestCase
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.utils import timezone

from categories.models import Category
from users.models import User
from .test_models import set_created_time
from ..forms import PostCreationForm
from ..models import Post


class AboutViewTestCase(TestCase):
    def test_use_correct_tempalte(self):
        response = self.client.get(reverse('forum:about'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'forum/about.html')


class ContactViewTestCase(TestCase):
    def test_use_correct_tempalte(self):
        response = self.client.get(reverse('forum:contact'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'forum/contact.html')


class DonateTestCase(TestCase):
    def test_use_correct_tempalte(self):
        response = self.client.get(reverse('forum:donate'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'forum/donate.html')


class ContentPreviewViewTestCase(TestCase):
    def test_preview_content_with_empty_content(self):
        response = self.client.post(reverse('forum:preview'), data={'content': ''})
        self.assertJSONEqual(response.content.decode(), json.dumps({'preview': ''}))

    def test_preview_content_with_non_empty_content(self):
        response = self.client.post(reverse('forum:preview'), data={'content': '# test h1 title'})
        self.assertJSONEqual(response.content.decode(),
                             json.dumps({'preview': '<h1 id="test-h1-title">test h1 title</h1>'}))


class IndexViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user', email='user@test.com', password='test8888')
        self.category = Category.objects.create(name='category', slug='category')
        self.post1 = Post.objects.create(title='post 1', category=self.category, author=self.user,
                                         created=set_created_time(minutes=3))
        self.post2 = Post.objects.create(title='post 2', category=self.category, author=self.user,
                                         created=set_created_time(minutes=2))
        self.post3 = Post.objects.create(title='post 3', category=self.category, author=self.user,
                                         created=set_created_time(minutes=1))

    def test_use_correct_template(self):
        response = self.client.get(reverse('forum:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'forum/index.html')

    def test_get_query_set(self):
        response = self.client.get(reverse('forum:index'))
        self.assertEqual(response.context['post_list'].count(), 3)


class PostDetailViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@test.com', password='test8888')
        self.category = Category.objects.create(name='test category', slug='test-category')
        self.post = Post.objects.create(
            title='test post',
            category=self.category,
            author=self.user,
        )
        self.removed_post = Post.objects.create(
            title='removed post',
            category=self.category,
            author=self.user,
            is_removed=True,
        )

    def test_use_correct_template(self):
        response = self.client.get(self.post.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'forum/detail.html')

    def test_can_only_visit_visible_post(self):
        response = self.client.get(self.removed_post.get_absolute_url())
        self.assertEqual(response.status_code, 404)

        response = self.client.get(self.post.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_increase_post_views(self):
        self.client.get(self.post.get_absolute_url())
        self.post.refresh_from_db()
        self.assertEqual(self.post.views, 1)

        self.client.get(self.post.get_absolute_url())
        self.post.refresh_from_db()
        self.assertEqual(self.post.views, 2)

    def test_get_context_data(self):
        ctype = ContentType.objects.get_for_model(self.post)
        response = self.client.get(self.post.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['ctype'], ctype)


class PostCreateViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@test.com', password='test8888')
        self.category = Category.objects.create(name='test category', slug='test-category')

    def test_redirect_anonymous_user_to_login_url(self):
        response = self.client.get(reverse('forum:create'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, settings.LOGIN_URL + '?next=/new/')

    def test_use_correct_template(self):
        self.client.login(username='testuser', password='test8888')
        response = self.client.get(reverse('forum:create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'forum/post_form.html')

    def test_no_initial_category(self):
        self.client.login(username='testuser', password='test8888')
        response = self.client.get(reverse('forum:create'))
        self.assertIsNone(response.context['form'].initial.get('category'))

    def test_has_initial_category(self):
        self.client.login(username='testuser', password='test8888')
        response = self.client.get(reverse('forum:create', kwargs={'slug': self.category.slug}))
        self.assertEqual(response.context['form'].initial.get('category'), self.category)

    def test_has_a_removed_or_non_exist_initial_category(self):
        category = Category.objects.create(name='removed category', slug='removed-category', is_removed=True)

        self.client.login(username='testuser', password='test8888')
        response = self.client.get(reverse('forum:create', kwargs={'slug': category.slug}))
        self.assertEqual(response.status_code, 404)

        response = self.client.get(reverse('forum:create', kwargs={'slug': 'non-exist'}))
        self.assertEqual(response.status_code, 404)

    def test_context_data(self):
        self.client.login(username='testuser', password='test8888')
        response = self.client.get(reverse('forum:create', kwargs={'slug': self.category.slug}))
        self.assertEqual(response.context['category'], self.category)

        # No initial category
        response = self.client.get(reverse('forum:create'))
        self.assertNotIn('category', response.context)

    def test_rate_limits(self):
        self.client.login(username='testuser', password='test8888')

        # too frequent rate
        data = {
            'title': 'test',
            'category': self.category.pk
        }
        response = self.client.post(reverse('forum:create'), data=data)
        self.assertEqual(response.status_code, 302)
        response = self.client.post(reverse('forum:create'), data=data)
        self.assertEqual(response.status_code, 403)

        Post.objects.all().delete()

        # Normal rate
        response = self.client.post(reverse('forum:create'), data=data)
        self.assertEqual(response.status_code, 302)
        post = Post.objects.first()
        post.created = post.created - timezone.timedelta(seconds=6)
        post.save()
        response = self.client.post(reverse('forum:create'), data=data)
        self.assertEqual(response.status_code, 302)


class PostEditViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@test.com', password='test8888')
        self.super_user = User.objects.create_superuser(username='superuser', email='superuser@test.com',
                                                        password='test8888')
        self.category = Category.objects.create(name='test category', slug='test-category')
        self.post = Post.objects.create(
            title='test post',
            category=self.category,
            author=self.user,
        )

    def test_redirect_anonymous_user_to_login_url(self):
        post = Post.objects.get(title='test post')
        response = self.client.get(reverse('forum:edit', kwargs={'pk': post.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, settings.LOGIN_URL + '?next=/post/%s/edit/' % post.pk)

    def test_use_correct_template(self):
        post = Post.objects.get(title='test post')
        self.client.login(username='testuser', password='test8888')
        response = self.client.get(reverse('forum:edit', kwargs={'pk': post.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'forum/post_edit_form.html')

    def test_edit_self_post(self):
        self.client.login(username='testuser', password='test8888')
        response = self.client.get(reverse('forum:edit', kwargs={'pk': self.post.pk}))
        self.assertEqual(response.status_code, 200)

    def test_can_not_edit_other_user_post(self):
        other_user = User.objects.create_user(username='otheruser', email='otheruser@test.com', password='test8888')
        post = Post.objects.create(
            title='test post',
            category=self.category,
            author=other_user,
        )
        self.client.login(username='testuser', password='test8888')
        response = self.client.get(reverse('forum:edit', kwargs={'pk': post.pk}))
        self.assertEqual(response.status_code, 403)

    def test_superuser_can_edit_all_posts(self):
        self.client.login(username='superuser', password='test8888')
        response = self.client.get(reverse('forum:edit', kwargs={'pk': self.post.pk}))
        self.assertEqual(response.status_code, 200)


class CategoryPostListViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@test.com', password='test8888')
        self.ancestor_category = Category.objects.create(name='ancestor category', slug='ancestor-category')
        self.parent_category = Category.objects.create(name='parent category', slug='parent-category',
                                                       parent=self.ancestor_category)
        self.child_category = Category.objects.create(name='child category', slug='child-category',
                                                      parent=self.parent_category)

    def test_use_correct_template(self):
        response = self.client.get(reverse('forum:category_posts', kwargs={'slug': 'ancestor-category'}))
        self.assertTemplateUsed(response, 'forum/index.html')

        response = self.client.get(reverse('forum:category_posts', kwargs={'slug': 'child-category'}))
        self.assertTemplateUsed(response, 'forum/category_post_list.html')

    def test_get_queryset(self):
        Post.objects.create(title='test post', category=self.parent_category, author=self.user)
        Post.objects.create(title='test post', category=self.child_category, author=self.user)

        response = self.client.get(reverse('forum:category_posts', kwargs={'slug': 'parent-category'}))
        self.assertEqual(response.context['post_list'].count(), 2)

        response = self.client.get(reverse('forum:category_posts', kwargs={'slug': 'child-category'}))
        self.assertEqual(response.context['post_list'].count(), 1)

    def test_get_context_data(self):
        response = self.client.get(reverse('forum:category_posts', kwargs={'slug': self.parent_category.slug}))
        self.assertQuerysetEqual(response.context['category_ancestors'],
                                 ['<Category: ancestor category>'])
        self.assertEqual(response.context['category'], self.parent_category)
        self.assertQuerysetEqual(response.context['category_children'], ['<Category: child category>'])
        self.assertIsInstance(response.context['form'], PostCreationForm)
        self.assertEqual(response.context['form'].initial['category'], self.parent_category)
