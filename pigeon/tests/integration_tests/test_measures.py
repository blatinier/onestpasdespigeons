import os
from django.contrib.auth.models import User
from django.test import Client, TestCase
from pigeon.settings import STATIC_ROOT
from weights.models import Measure


class MeasureTestCase(TestCase):
    fixtures = ['user.json', 'products.json', 'measures.json']

    def setUp(self):
        self.client = Client()
        self.client.force_login(User.objects.get(username="test_user_1"))

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
                                     "unit": "g",
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
        measure_id = Measure.objects.latest('id').id
        resp = self.client.get("/edit_measure/%d" % measure_id)
        self.assertIn(b'Edit', resp.content)
        with open(os.path.join(STATIC_ROOT, 'images', 'benoit.png'), 'rb') as data:
            resp = self.client.post("/edit_measure/%d" % measure_id,
                                    {"product": "0000000003087",
                                     "unit": "oz",
                                     "package_weight": 1000,
                                     "measured_weight": 800,
                                     "measure_image": data},
                                    format="multipart",
                                    follow=True)
        self.assertIn(b"Measure edited!", resp.content)
        self.assertIn(b"800", resp.content)
        self.assertIn(b"oz", resp.content)

        # Delete measure
        resp = self.client.get("/delete_measure/%d" % measure_id, follow=True)
        self.assertIn(b"Measure deleted!", resp.content)
        self.assertNotIn(b"Farine de bl\xc3\xa9 noir", resp.content)

    def test_add_and_continue(self):
        """
        Test the following steps:
        - Add a measure
        - Check on add measure again
        """
        # Add measure
        with open(os.path.join(STATIC_ROOT, 'images', 'benoit.png'), 'rb') as data:
            resp = self.client.post("/add_measure",
                                    {"product": "0000000003087",
                                     "unit": "g",
                                     "package_weight": 1000,
                                     "measured_weight": 900,
                                     "measure_image": data,
                                     "add_and_continue": True},
                                    format="multipart",
                                    follow=True)

        # Check added and redirected
        self.assertIn(b'Add a measure', resp.content)
        self.assertIn(b"Measure added!", resp.content)
        self.assertEqual(resp.redirect_chain, [("/add_measure", 302)])

    def test_delete_measure_not_owned(self):
        """
        Try to delete measure not owned
        """
        # Create a measure
        with open(os.path.join(STATIC_ROOT, 'images', 'benoit.png'), 'rb') as data:
            resp = self.client.post("/add_measure",
                                    {"product": "0000000003087",
                                     "unit": "g",
                                     "package_weight": 1000,
                                     "measured_weight": 900,
                                     "measure_image": data},
                                    format="multipart",
                                    follow=True)
        # Change user
        self.client.force_login(User.objects.get(username="test_user_2"))

        # Try to delete measure
        measure = Measure.objects.filter(product="0000000003087")[0]

        resp = self.client.get("/delete_measure/%d" % measure.id, follow=True)
        self.assertEqual(resp.status_code, 403)

    def test_sort(self):
        resp1 = self.client.get('/list_measures',
                                {'order_by': 'pweight', 'sort_order': 'asc'})
        resp2 = self.client.get('/list_measures',
                                {'order_by': 'pweight', 'sort_order': 'desc'})

        self.assertTrue(resp1.content != resp2.content)

    def test_add_create_product(self):
        """
        Try to add a measure with product creation
        Try to add a measure without product creation or selection (should fail)
        """
        # Add measure with product
        with open(os.path.join(STATIC_ROOT, 'images', 'benoit.png'), 'rb') as data:
            resp = self.client.post("/add_measure",
                                    {"code": "45678987654",
                                     "product_name": "pipo product",
                                     "brands": "pipo brands",
                                     "unit": "g",
                                     "package_weight": 1000,
                                     "measured_weight": 900,
                                     "measure_image": data},
                                    format="multipart",
                                    follow=True)

        # Check added and redirected
        self.assertIn(b"My measures", resp.content)
        self.assertIn(b"Measure added!", resp.content)
        self.assertIn(b"pipo product", resp.content)
        self.assertEqual(resp.redirect_chain, [("/my_measures", 302)])

        # Add measure without product
        with open(os.path.join(STATIC_ROOT, 'images', 'benoit.png'), 'rb') as data:
            resp = self.client.post("/add_measure",
                                    {"unit": "g",
                                     "package_weight": 1000,
                                     "measured_weight": 900,
                                     "measure_image": data},
                                    format="multipart",
                                    follow=True)

        self.assertIn(b"Add a measure", resp.content)
        self.assertIn(b"Please select or create a product", resp.content)
