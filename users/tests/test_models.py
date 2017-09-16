import os

from django.test import TestCase

from ..models import User, user_mugshot_path


# TODO: test mugshot
class UserModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@test.com', password='test8888')

    def test_user_mugshot_path(self):
        self.assertEqual(user_mugshot_path(self.user, 'default_mugshot.png'),
                         os.path.join('mugshots', self.user.username, 'default_mugshot.png'))

    def test_str(self):
        self.assertEqual(self.user.__str__(), 'testuser')

    def test_save_user_without_nickname(self):
        self.assertEqual(self.user.nickname, self.user.username)

    def test_save_user_with_nickname(self):
        user = User.objects.create_user(username='user', email='user@test.com', password='test8888',
                                        nickname='nick')
        self.assertEqual(user.nickname, 'nick')
