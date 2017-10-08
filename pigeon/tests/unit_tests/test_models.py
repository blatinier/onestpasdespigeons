from django.test import TestCase
from weights.models import Measure, Product, PigeonUser


class MeasureTestCase(TestCase):
    def setUp(self):
        self.user = PigeonUser.objects.create(username="pipo")
        self.user.refresh_from_db()
        self.product = Product.objects.create(code="TEST",
                                              product_name="TEST_PRODUCTA",
                                              generic_name="TEST_PRODUCTB")
        self.measure = Measure.objects.create(user=self.user,
                                              product=self.product,
                                              package_weight=10,
                                              measured_weight=9)


    def test_measure_diff(self):
        """Measures diff tests"""
        self.assertEqual(self.measure.diff, -1)
        self.assertAlmostEqual(self.measure.percent_diff, -10)
