from django.test import TestCase

from .models import Category


class CategoryTestCase(TestCase):
    def test_str(self):
        category_en = Category.objects.create(name='test category', slug='test-category-en')
        category_zh = Category.objects.create(name='测试分类', slug='test-category-zh')

        self.assertEqual(str(category_en), 'test category')
        self.assertEqual(str(category_zh), '测试分类')

    def test_default_manager(self):
        Category.objects.create(name='removed', slug='removed', is_removed=True)
        Category.objects.create(name='visible', slug='visible')

        self.assertQuerysetEqual(Category.objects.all().order_by('name'),
                                 ['<Category: removed>', '<Category: visible>'])

    def test_public_manager(self):
        Category.objects.create(name='removed', slug='removed', is_removed=True)
        Category.objects.create(name='visible', slug='visible')

        self.assertQuerysetEqual(Category.public.all(), ['<Category: visible>'])

    def test_soft_bulk_delete(self):
        Category.objects.create(name='category-1', slug='category-1')
        Category.objects.create(name='category-2', slug='category-2')

        Category.public.all().delete()
        self.assertEqual(Category.public.count(), 0)
        self.assertQuerysetEqual(Category.objects.all().order_by('name'),
                                 ['<Category: category-1>', '<Category: category-2>'])

    def test_soft_object_delete(self):
        category = Category.objects.create(name='category', slug='category')
        category.delete()
        self.assertEqual(Category.public.count(), 0)
        self.assertQuerysetEqual(Category.objects.all(), ['<Category: category>'])
