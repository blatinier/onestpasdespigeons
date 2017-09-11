import os
from django.contrib.auth.models import User
from django.test import Client, TestCase
from pigeon.settings import STATIC_ROOT
from weights.models import Measure


class ProductPageTestCase(TestCase):
    fixtures = ['user.json', 'products.json', 'measures.json']

    def setUp(self):
        self.client = Client()
        self.client.force_login(User.objects.get(username="test_user_1"))

    def test_view_product(self):
        """
        Test informations showed
        """
        resp = self.client.get("/product/0000000016124")
        self.assertEqual(resp.status_code, 200)
        # product name shown
        self.assertIn(b'Organic Muesli', resp.content)
        # brands shown
        self.assertIn(b"Daddy&#39;s Muesli", resp.content)
        # number of measures shown
        self.assertIn(b'<span class="big">2</span>', resp.content)
        # average diff shown
        self.assertIn(b"-17.5 %", resp.content)
        # measures shown
        self.assertIn(b'upload/measures/test_user_1/img11.jpg', resp.content)
        self.assertIn(b'upload/measures/test_user_1/img1.jpg', resp.content)