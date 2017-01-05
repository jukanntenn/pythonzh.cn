from django.test import TestCase
from django.urls import reverse

from categories.models import Category
from users.models import User
from ..forms import PostCreationForm
from ..models import Post


class CategoryPostListViewTestCase(TestCase):
    def test_can_only_visit_visible_category(self):
        Category.objects.create(name='removed', slug='removed', is_removed=True)
        Category.objects.create(name='visible', slug='visible')

        response = self.client.get(reverse('forum:category_posts', kwargs={'slug': 'removed'}))
        self.assertEqual(response.status_code, 404)

        response = self.client.get(reverse('forum:category_posts', kwargs={'slug': 'visible'}))
        self.assertEqual(response.status_code, 200)

    def test_use_correct_template(self):
        Category.objects.create(name='category test', slug='category-test')

        response = self.client.get(reverse('forum:category_posts', kwargs={'slug': 'category-test'}))
        self.assertTemplateUsed(response, 'forum/category_post_list.html')

    def test_get_context_data(self):
        ancestor_category = Category.objects.create(name='ancestor category', slug='ancestor-category', )
        category = Category.objects.create(name='category', slug='category', parent=ancestor_category)
        Category.objects.create(name='child category',
                                slug='child-category',
                                parent=category)

        response = self.client.get(reverse('forum:category_posts', kwargs={'slug': category.slug}))
        self.assertQuerysetEqual(response.context['category_ancestors'],
                                 ['<Category: ancestor category>'])
        self.assertEqual(response.context['category'], category)
        self.assertQuerysetEqual(response.context['category_children'], ['<Category: child category>'])
        self.assertIsInstance(response.context['form'], PostCreationForm)
        self.assertEqual(response.context['form'].initial['category'], category)


class IndexViewTestCase(TestCase):
    def test_use_correct_template(self):
        response = self.client.get(reverse('forum:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'forum/index.html')

    def test_template_context_data(self):
        pass


class PostDetailViewTestCase(TestCase):
    def test_use_correct_template(self):
        user = User.objects.create_user(username='testuser', email='test@test.com', password='test8888')
        category = Category.objects.create(name='test category', slug='test-category')
        post = Post.objects.create(
            title='test post',
            category=category,
            author=user,
        )

        response = self.client.get(post.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'forum/detail.html')

    def test_can_only_visit_visible_post(self):
        user = User.objects.create_user(username='testuser', email='test@test.com', password='test8888')
        category = Category.objects.create(name='test category', slug='test-category')
        removed_post = Post.objects.create(
            title='removed post',
            category=category,
            author=user,
            is_removed=True,
        )
        visible_post = Post.objects.create(
            title='visible post',
            category=category,
            author=user,
        )

        response = self.client.get(removed_post.get_absolute_url())
        self.assertEqual(response.status_code, 404)

        response = self.client.get(visible_post.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_increase_post_views(self):
        user = User.objects.create_user(username='testuser', email='test@test.com', password='test8888')
        category = Category.objects.create(name='test category', slug='test-category')
        post = Post.objects.create(
            title='test post',
            category=category,
            author=user,
        )

        self.client.get(post.get_absolute_url())
        post.refresh_from_db()

        self.assertEqual(post.views, 1)

    def test_get_context_data(self):
        pass
