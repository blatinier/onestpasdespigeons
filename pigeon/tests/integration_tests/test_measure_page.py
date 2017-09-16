from django.contrib.auth.models import User
from django.test import Client, TestCase


class MeasurePageTestCase(TestCase):
    fixtures = ['user.json', 'products.json', 'measures.json']

    def setUp(self):
        self.client = Client()
        self.client.force_login(User.objects.get(username="test_user_1"))

    def test_view_measure(self):
        """
        Test informations showed
        """
        resp = self.client.get("/measure/1")
        self.assertEqual(resp.status_code, 200)
        # product name shown
        self.assertIn(b'Organic Muesli', resp.content)
        # brands shown
        self.assertIn(b"Daddy&#39;s Muesli", resp.content)
        # measure id shown
        self.assertIn(b'#1', resp.content)
        # diff shown
        self.assertIn(b"-10.0 %", resp.content)
