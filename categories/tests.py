from django.test import TestCase

from .models import Category


class CategoryTestCase(TestCase):
    def test__str__(self):
        category_en = Category.objects.create(name='test category', slug='test-category-en')
        category_zh = Category.objects.create(name='测试分类', slug='test-category-zh')

        self.assertEqual(category_en.__str__(), 'test category')
        self.assertEqual(category_zh.__str__(), '测试分类')

    def test_manager_visible(self):
        Category.objects.create(name='removed', slug='removed', is_removed=True)
        Category.objects.create(name='visible', slug='visible')

        self.assertQuerysetEqual(Category.objects.visible(), ['<Category: visible>'])
