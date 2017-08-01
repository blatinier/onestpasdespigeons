import os
from django.contrib.auth.models import User
from django.test import Client, TestCase
from pigeon.settings import STATIC_ROOT


class AuthTestCase(TestCase):
    fixtures = ['user.json', 'products.json']

    def setUp(self):
        self.client = Client()
        self.client.force_login(User.objects.get(username="ab"))

    def test_add_edit_list_delete(self):
        """
        Test the following steps:
        - Add a measure
        - Edit a measure
        - List measure
        - Delete measure
        """
        # Go to listing
        resp = self.client.get("/my_measures")
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b'My measures', resp.content)

        # Go to add form
        resp = self.client.get("/add_measure")
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b'Add a measure', resp.content)

        # Add measure
        with open(os.path.join(STATIC_ROOT, 'images', 'benoit.png'), 'rb') as data:
            resp = self.client.post("/add_measure",
                                    {"product": "0000000003087",
                                     "package_weight": 1000,
                                     "measured_weight": 900,
                                     "measure_image": data},
                                    format="multipart",
                                    follow=True)

        # Check added and redirected
        self.assertIn(b"My measures", resp.content)
        self.assertIn(b"Measure added!", resp.content)
        self.assertIn(b"Farine de bl\xc3\xa9 noir", resp.content)
        self.assertEqual(resp.redirect_chain, [("/my_measures", 302)])

        # Go to edit measure
        resp = self.client.get("/edit_measure/1")
        self.assertIn(b'Edit', resp.content)
        with open(os.path.join(STATIC_ROOT, 'images', 'benoit.png'), 'rb') as data:
            resp = self.client.post("/edit_measure/1",
                                    {"product": "0000000003087",
                                     "package_weight": 1000,
                                     "measured_weight": 800,
                                     "measure_image": data},
                                    format="multipart",
                                    follow=True)
        self.assertIn(b"Measure edited!", resp.content)
        self.assertIn(b"800", resp.content)
        # Delete measure
        resp = self.client.get("/delete_measure/1", follow=True)
        self.assertIn(b"Measure deleted!", resp.content)
        self.assertNotIn(b"Farine de bl\xc3\xa9 noir", resp.content)
