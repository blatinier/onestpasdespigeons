from weights.models import PigeonUser
from django.test import Client, TestCase
from unittest import skipIf
from django.db import connection


class OverviewTestCase(TestCase):
    fixtures = ['user.json', 'products.json', 'measures.json']

    def setUp(self):
        self.client = Client()
        self.client.force_login(PigeonUser.objects.get(username="test_user_1"))

    @skipIf(connection.vendor == 'sqlite', 'Aggregations have not the same precision on sqlite')
    def test_add_edit_list_delete(self):
        """
        Check overview statistics
        """
        resp = self.client.get("/en/overview")
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b'Overview', resp.content)
        self.assertIn(b'# Products: 101', resp.content)
        self.assertIn(b'# Measures: 11', resp.content)
        self.assertIn(b'Min difference: -150', resp.content)
        self.assertIn(b'Max difference: 100', resp.content)
        self.assertIn(b'Median difference: -50', resp.content)
        self.assertIn(b'Mean difference: -50', resp.content)
        self.assertIn(b'Min difference: -25.0%', resp.content)
        self.assertIn(b'Max difference: 16.67%', resp.content)
        self.assertIn(b'Median difference: -10.0%', resp.content)
        self.assertIn(b'Mean difference: -8.25%', resp.content)
        self.assertIn(b'Organic Shoyu (San J): 16.67 %', resp.content)
        self.assertIn(b'Organic Sunflower Oil (Napa Valley Naturals): -25.00 %', resp.content)
