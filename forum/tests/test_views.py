from django.test import TestCase
from django.urls import reverse

from categories.models import Category
from ..forms import PostCreationForm


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

        # def test_do_not_display_posts_in_removed_category(self):
        #     removed_category = Category.objects.create(name='removed', slug='removed', is_removed=True)
        #     visible_category = Category.objects.create(name='visible', slug='visible')

    def test_get_context_data(self):
        ancestor_category = Category.objects.create(name='ancestor category', slug='ancestor-category', )
        category = Category.objects.create(name='category', slug='category', parent=ancestor_category)
        Category.objects.create(name='child category',
                                slug='child-category',
                                parent=category)

        response = self.client.get(reverse('forum:category_posts', kwargs={'slug': category.slug}))
        self.assertQuerysetEqual(response.context['category_ancestors'],
                                 ['<Category: ancestor category>', '<Category: category>'])
        self.assertEqual(response.context['category'], category)
        self.assertQuerysetEqual(response.context['category_children'], ['<Category: child category>'])
        self.assertIsInstance(response.context['form'], PostCreationForm)
        self.assertEqual(response.context['form'].initial['category'], category)
