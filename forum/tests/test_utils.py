import unittest

from django.test import TestCase

from users.models import User
from ..utils import bleach_value, markdown_value, parse_nicknames


class BleachValueTestCase(unittest.TestCase):
    def test_bleach_value(self):
        value = """
        <h1>h1 title</h1><script>alter('evil script')</script>
        """
        expected_value = """
        <h1>h1 title</h1>&lt;script&gt;alter('evil script')&lt;/script&gt;
        """
        self.assertEqual(bleach_value(value), expected_value)


class MarkdownValueTestCase(unittest.TestCase):
    def test_markdown_value(self):
        value = "# h1 test\n## h2 test"
        expected_value = '<h1 id="h1-test">h1 test</h1>\n<h2 id="h2-test">h2 test</h2>'
        self.assertEqual(markdown_value(value), expected_value)


class ParserNicknamesTestCase(TestCase):
    def test_parse_nicknames(self):
        user = User.objects.create_user('user', 'user@test.com', 'user1234')
        user_url = user.get_absolute_url()
        value = "@[%s](%s)" % (user.pk, user_url)
        self.assertEqual(parse_nicknames(value), "@[%s](%s)" % (user.nickname, user_url))
