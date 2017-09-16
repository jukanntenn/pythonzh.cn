from django.test import TestCase

from .models import Category


class CategoryTestCase(TestCase):
    def setUp(self):
        self.visible_category = Category.objects.create(name='visible', slug='visible')
        self.removed_category = Category.objects.create(name='removed', slug='removed', is_removed=True)

    def test_str(self):
        self.assertEqual(str(self.visible_category), 'visible')

    def test_objects_manager(self):
        self.assertQuerysetEqual(Category.objects.all().order_by('name'),
                                 ['<Category: removed>', '<Category: visible>'])

    def test_public_manager(self):
        self.assertQuerysetEqual(Category.public.all(), ['<Category: visible>'])

    def test_soft_bulk_delete_objects(self):
        Category.public.all().delete()
        self.assertEqual(Category.public.count(), 0)
        self.assertQuerysetEqual(Category.objects.all().order_by('name'),
                                 ['<Category: removed>', '<Category: visible>'])

    def test_soft_delete_object(self):
        self.visible_category.delete()
        self.removed_category.delete()

        self.assertEqual(Category.public.count(), 0)
        self.assertQuerysetEqual(Category.objects.all().order_by('name'),
                                 ['<Category: removed>', '<Category: visible>'])
