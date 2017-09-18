import os
from weights.models import PigeonUser
from django.test import Client, TestCase
from weights.models import Measure
from tests import TEST_IMAGE_PATH

class ProfilePageTestCase(TestCase):
    fixtures = ['user.json', 'products.json', 'measures.json']

    def setUp(self):
        self.client = Client()
        self.client.force_login(PigeonUser.objects.get(username="test_user_1"))

    def test_view_profile(self):
        """
        Test informations showed
        """
        resp = self.client.get("/en/profile/11111111/test_user_1")
        self.assertEqual(resp.status_code, 200)
        # username shown
        self.assertIn(b'test_user_1', resp.content)
        # no avatar -> fallback avatar shown
        self.assertIn(b'pigeon-anon.svg', resp.content)
        # measures shown
        self.assertIn(b'static/images/logo.png', resp.content)

        # set an avatar and a pseudo
        with open(TEST_IMAGE_PATH, 'rb') as data:
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
            resp = self.client.post('/en/account', new_user_data, follow=True, format="multipart")

        resp = self.client.get("/en/profile/11111111/test_user_1")
        # username shown
        self.assertIn(b'pouet', resp.content)
        # no avatar -> fallback avatar shown
        self.assertIn(b'/upload/avatar/test_user_1', resp.content)
