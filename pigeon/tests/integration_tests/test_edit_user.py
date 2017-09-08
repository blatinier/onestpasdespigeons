import os
from django.contrib.auth import get_user
from django.contrib.auth.models import User
from django.test import Client, TestCase
from pigeon.settings import STATIC_ROOT


class EditUserTestCase(TestCase):
    fixtures = ['user.json']

    def setUp(self):
        self.client = Client()
        self.client.force_login(User.objects.get(username="test_user_1"))

    def test_successful_update(self):
        # Go to edit user page
        resp = self.client.get("/account")
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b'Edit my account', resp.content)

        with open(os.path.join(STATIC_ROOT, 'images', 'benoit.png'), 'rb') as data:
            new_user_data = {'user-username': 'aaa',
                             'user-first_name': 'bbb',
                             'user-last_name': 'ccc',
                             'user-email': 'pipo@pouet.com',
                             'user-password1': 'pipopouet42',
                             'user-password2': 'pipopouet42',
                             'profile-language': 'fr',
                             'profile-country': 'us',
                             'profile-nickname': 'pouet',
                             'profile-avatar': data,
                             }

            resp = self.client.post('/account', new_user_data, follow=True, format="multipart")

        self.assertIn(b'Update successful', resp.content)

        user = get_user(self.client)
        self.assertTrue(user.is_authenticated())
        self.assertEquals(user.username, 'aaa')
        self.assertEquals(user.first_name, 'bbb')
        self.assertEquals(user.last_name, 'ccc')
        self.assertEquals(user.email, 'pipo@pouet.com')
        self.assertEquals(user.pigeonuser.language, 'fr')
        self.assertEquals(user.pigeonuser.country, 'us')
        self.assertEquals(user.pigeonuser.nickname, 'pouet')
        self.assertTrue(user.pigeonuser.avatar.url.startswith('upload/avatar/aaa/benoit'))

    def test_failure_update(self):
        # Go to edit user page
        resp = self.client.get("/account")
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b'Edit my account', resp.content)

        new_user_data = {'user-username': '',  # Will normally fail!
                         'user-first_name': 'bbb',
                         'user-last_name': 'ccc',
                         'user-email': 'pipo@pouet.com',
                         'user-password1': '',
                         'user-password2': '',
                         'profile-language': 'fr',
                         'profile-country': 'us',
                         }

        resp = self.client.post('/account', new_user_data, follow=True)

        self.assertIn(b'This field is required', resp.content)

        user = get_user(self.client)
        self.assertTrue(user.is_authenticated())
        self.assertNotEquals(user.username, '')
