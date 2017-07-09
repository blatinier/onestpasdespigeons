from django.db import models


class Product(models.Model):
    """
    https://world.openfoodfacts.org/data/data-fields.txt
    """
    # models which source is from OFF and should be updated accordingly
    sourced_OFF_fields = ["url_OFF", "product_name", "generic_name",
                          "quantity", "packaging", "packaging_tags",
                          "brands", "brands_tags", "categories",
                          "categories_tags", "categories_fr", "labels",
                          "labels_tags", "labels_fr", "purchase_places",
                          "image_url"]

    # barcode, if it starts with "200" it's a OFF custom code provided
    # and barcode is not known yet
    code = models.CharField(max_length=64, db_index=True, primary_key=True)
    url_OFF = models.CharField(max_length=1024)
    product_name = models.CharField(max_length=512, db_index=True)
    generic_name = models.CharField(max_length=1024, db_index=True)
    quantity = models.CharField(max_length=512, blank=True, null=True)

    packaging = models.CharField(max_length=512, blank=True, null=True)  # shape, material
    packaging_tags = models.CharField(max_length=512, blank=True, null=True)
    brands = models.CharField(max_length=512, blank=True, null=True)
    brands_tags = models.CharField(max_length=512, blank=True, null=True)
    categories = models.CharField(max_length=1024, blank=True, null=True)
    categories_tags = models.CharField(max_length=1024, blank=True, null=True)
    categories_fr = models.CharField(max_length=1024, blank=True, null=True)
    labels = models.CharField(max_length=1024, blank=True, null=True)
    labels_tags = models.CharField(max_length=1024, blank=True, null=True)
    labels_fr = models.CharField(max_length=1024, blank=True, null=True)
    purchase_places = models.CharField(max_length=256, blank=True, null=True)
    image_url = models.CharField(max_length=256, blank=True, null=True)

    def copy(self):
        """
        Dump all models
        """
        dump = {}
        for attr in self._data:
            dump[attr] = getattr(self, attr)
        return self.__class__(**dump)

    def update_with_OFF_product(self, product_off):
        """
        Parse OFF product (which is the same model) and update current
        product with
        """
        for field in self.sourced_OFF_fields:
            off_field = getattr(product_off, field)
            if off_field != getattr(self, field):
                setattr(self, field, off_field)
