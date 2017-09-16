import unittest

from django.core.paginator import Paginator

from ..mixins import PaginationMixin


class PaginationMixinTestCase(unittest.TestCase):
    def setUp(self):
        self.objects = ['Django', 'Flask', 'Requests', 'unittest', 'urllib', 'selenium', 'redis', 'scrapy', 'numpy']
        self.paginator = Paginator(self.objects, 9)
        self.page = self.paginator.page(1)
        self.pagination_mixin = PaginationMixin()

    def test_does_not_paginated(self):
        self.assertEqual(self.pagination_mixin.pagination_data(self.paginator, self.page, False), {})

    def test_page_number_equals_1_and_only_1_page(self):
        self.assertDictEqual(self.pagination_mixin.pagination_data(self.paginator, self.page, True),
                             {
                                 'left': [],
                                 'right': [],
                                 'left_has_more': False,
                                 'right_has_more': False,
                                 'first': False,
                                 'last': False,
                             })

    def test_page_number_equals_1_and_3_pages(self):
        self.paginator = Paginator(self.objects, 3)
        self.assertDictEqual(self.pagination_mixin.pagination_data(self.paginator, self.page, True),
                             {
                                 'left': [],
                                 'right': [2, 3],
                                 'left_has_more': False,
                                 'right_has_more': False,
                                 'first': False,
                                 'last': False,
                             })

    def test_page_number_equals_1_and_4_pages(self):
        self.objects.remove('numpy')
        self.paginator = Paginator(self.objects, 2)
        self.assertDictEqual(self.pagination_mixin.pagination_data(self.paginator, self.page, True),
                             {
                                 'left': [],
                                 'right': [2, 3],
                                 'left_has_more': False,
                                 'right_has_more': False,
                                 'first': False,
                                 'last': True,
                             })

    def test_page_number_equals_1_and_more_than_5_pages(self):
        self.paginator = Paginator(self.objects, 1)
        self.assertDictEqual(self.pagination_mixin.pagination_data(self.paginator, self.page, True),
                             {
                                 'left': [],
                                 'right': [2, 3],
                                 'left_has_more': False,
                                 'right_has_more': True,
                                 'first': False,
                                 'last': True,
                             })

    def test_page_number_equals_total_pages_and_only_1_page(self):
        self.assertDictEqual(self.pagination_mixin.pagination_data(self.paginator, self.page, True),
                             {
                                 'left': [],
                                 'right': [],
                                 'left_has_more': False,
                                 'right_has_more': False,
                                 'first': False,
                                 'last': False,
                             })

    def test_page_number_equals_total_pages_and_3_pages(self):
        self.paginator = Paginator(self.objects, 3)
        self.page = self.paginator.page(self.paginator.num_pages)
        self.assertDictEqual(self.pagination_mixin.pagination_data(self.paginator, self.page, True),
                             {
                                 'left': [1, 2],
                                 'right': [],
                                 'left_has_more': False,
                                 'right_has_more': False,
                                 'first': False,
                                 'last': False,
                             })

    def test_page_number_equals_total_pages_and_4_pages(self):
        self.objects.remove('numpy')
        self.paginator = Paginator(self.objects, 2)
        self.page = self.paginator.page(self.paginator.num_pages)
        self.assertDictEqual(self.pagination_mixin.pagination_data(self.paginator, self.page, True),
                             {
                                 'left': [2, 3],
                                 'right': [],
                                 'left_has_more': False,
                                 'right_has_more': False,
                                 'first': True,
                                 'last': False,
                             })

    def test_page_number_equals_total_pages_and_more_than_5_pages(self):
        self.paginator = Paginator(self.objects, 1)
        self.page = self.paginator.page(self.paginator.num_pages)
        self.assertDictEqual(self.pagination_mixin.pagination_data(self.paginator, self.page, True),
                             {
                                 'left': [7, 8],
                                 'right': [],
                                 'left_has_more': True,
                                 'right_has_more': False,
                                 'first': True,
                                 'last': False,
                             })

    def test_page_number_not_an_edge_and_3_pages(self):
        # 1 2 3
        self.paginator = Paginator(self.objects, 3)
        self.page = self.paginator.page(2)
        self.assertDictEqual(self.pagination_mixin.pagination_data(self.paginator, self.page, True),
                             {
                                 'left': [1],
                                 'right': [3],
                                 'left_has_more': False,
                                 'right_has_more': False,
                                 'first': False,
                                 'last': False,
                             })

    def test_page_number_not_an_edge_and_4_pages(self):
        # 1 2 3 4
        self.objects.remove('numpy')
        self.paginator = Paginator(self.objects, 2)
        self.page = self.paginator.page(3)
        self.assertDictEqual(self.pagination_mixin.pagination_data(self.paginator, self.page, True),
                             {
                                 'left': [1, 2],
                                 'right': [4],
                                 'left_has_more': False,
                                 'right_has_more': False,
                                 'first': False,
                                 'last': False,
                             })

    def test_page_number_equals_2_and_5_pages(self):
        # 1 2 3 4 5
        self.paginator = Paginator(self.objects, 2)
        self.page = self.paginator.page(2)
        self.assertDictEqual(self.pagination_mixin.pagination_data(self.paginator, self.page, True),
                             {
                                 'left': [1],
                                 'right': [3, 4],
                                 'left_has_more': False,
                                 'right_has_more': False,
                                 'first': False,
                                 'last': True,
                             })

    def test_page_number_equals_3_and_5_pages(self):
        # 1 2 3 4 5
        self.paginator = Paginator(self.objects, 2)
        self.page = self.paginator.page(3)
        self.assertDictEqual(self.pagination_mixin.pagination_data(self.paginator, self.page, True),
                             {
                                 'left': [1, 2],
                                 'right': [4, 5],
                                 'left_has_more': False,
                                 'right_has_more': False,
                                 'first': False,
                                 'last': False,
                             })

    def test_page_number_equals_4_and_5_pages(self):
        # 1 2 3 4 5
        self.paginator = Paginator(self.objects, 2)
        self.page = self.paginator.page(4)
        self.assertDictEqual(self.pagination_mixin.pagination_data(self.paginator, self.page, True),
                             {
                                 'left': [2, 3],
                                 'right': [5],
                                 'left_has_more': False,
                                 'right_has_more': False,
                                 'first': True,
                                 'last': False,
                             })

    def test_page_number_equals_2_and_9_pages(self):
        # 1 2 3 4 5 6 7 8 9
        self.paginator = Paginator(self.objects, 1)
        self.page = self.paginator.page(2)
        self.assertDictEqual(self.pagination_mixin.pagination_data(self.paginator, self.page, True),
                             {
                                 'left': [1],
                                 'right': [3, 4],
                                 'left_has_more': False,
                                 'right_has_more': True,
                                 'first': False,
                                 'last': True,
                             })

    def test_page_number_equals_4_and_9_pages(self):
        # 1 2 3 4 5 6 7 8 9
        self.paginator = Paginator(self.objects, 1)
        self.page = self.paginator.page(4)
        self.assertDictEqual(self.pagination_mixin.pagination_data(self.paginator, self.page, True),
                             {
                                 'left': [2, 3],
                                 'right': [5, 6],
                                 'left_has_more': False,
                                 'right_has_more': True,
                                 'first': True,
                                 'last': True,
                             })

    def test_page_number_equals_5_and_9_pages(self):
        # 1 2 3 4 5 6 7 8 9
        self.paginator = Paginator(self.objects, 1)
        self.page = self.paginator.page(5)
        self.assertDictEqual(self.pagination_mixin.pagination_data(self.paginator, self.page, True),
                             {
                                 'left': [3, 4],
                                 'right': [6, 7],
                                 'left_has_more': True,
                                 'right_has_more': True,
                                 'first': True,
                                 'last': True,
                             })

    def test_page_number_equals_7_and_9_pages(self):
        # 1 2 3 4 5 6 7 8 9
        self.paginator = Paginator(self.objects, 1)
        self.page = self.paginator.page(7)
        self.assertDictEqual(self.pagination_mixin.pagination_data(self.paginator, self.page, True),
                             {
                                 'left': [5, 6],
                                 'right': [8, 9],
                                 'left_has_more': True,
                                 'right_has_more': False,
                                 'first': True,
                                 'last': False,
                             })
