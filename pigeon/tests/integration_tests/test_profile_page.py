import os
from django.contrib.auth.models import User
from django.test import Client, TestCase
from pigeon.settings import STATIC_ROOT


class ProfilePageTestCase(TestCase):
    fixtures = ['user.json', 'products.json', 'measures.json']

    def setUp(self):
        self.client = Client()
        self.client.force_login(User.objects.get(username="test_user_1"))

    def test_view_profile(self):
        """
        Test informations showed
        """
        resp = self.client.get("/profile/11111111/test_user_1")
        self.assertEqual(resp.status_code, 200)
        # username shown
        self.assertIn(b'test_user_1', resp.content)
        # no avatar -> fallback avatar shown
        self.assertIn(b'pigeon-anon.svg', resp.content)
        # measures shown
        self.assertIn(b'upload/measures/test_user_1/img11.jpg', resp.content)

        # set an avatar and a pseudo
        with open(os.path.join(STATIC_ROOT, 'images', 'benoit.png'), 'rb') as data:
            new_user_data = {'user-username': 'test_user_1',
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

        resp = self.client.get("/profile/11111111/test_user_1")
        # username shown
        self.assertIn(b'pouet', resp.content)
        # no avatar -> fallback avatar shown
        self.assertIn(b'/upload/avatar/test_user_1', resp.content)
