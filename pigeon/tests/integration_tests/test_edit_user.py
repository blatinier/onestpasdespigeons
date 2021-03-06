import os
from django.contrib.auth import get_user
from weights.models import PigeonUser
from django.test import Client, TestCase
from tests import TEST_IMAGE_PATH

class EditPigeonUserTestCase(TestCase):
    fixtures = ['user.json']

    def setUp(self):
        self.client = Client()
        self.client.force_login(PigeonUser.objects.get(username="test_user_1"))

    def test_successful_update(self):
        # Go to edit user page
        resp = self.client.get("/en/account")
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b'Edit my account', resp.content)

        with open(TEST_IMAGE_PATH, 'rb') as data:
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

            resp = self.client.post('/en/account', new_user_data, follow=True, format="multipart")

        self.assertIn(b'Update successful', resp.content)

        user = get_user(self.client)
        self.assertTrue(user.is_authenticated())
        self.assertEquals(user.username, 'aaa')
        self.assertEquals(user.first_name, 'bbb')
        self.assertEquals(user.last_name, 'ccc')
        self.assertEquals(user.email, 'pipo@pouet.com')
        self.assertEquals(user.language, 'fr')
        self.assertEquals(user.country, 'us')
        self.assertEquals(user.nickname, 'pouet')
        self.assertTrue(user.avatar.url.startswith('upload/avatar/aaa/benoit'))

    def test_failure_update(self):
        # Go to edit user page
        resp = self.client.get("/en/account")
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

        resp = self.client.post('/en/account', new_user_data, follow=True)

        self.assertIn(b'This field is required', resp.content)

        user = get_user(self.client)
        self.assertTrue(user.is_authenticated())
        self.assertNotEquals(user.username, '')
