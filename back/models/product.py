from mongoengine import Document, fields


class Product(Document):
    """
    https://world.openfoodfacts.org/data/data-fields.txt
    """
    meta = {
        'collection': 'products',
        'indexes': [
            "code",
            "product_name",
            "generic_name"
        ],
        'strict': False  # Ignore extra fields
    }

    # fields which source is from OFF and should be updated accordingly
    sourced_OFF_fields = ["url_OFF", "product_name", "generic_name",
                          "quantity", "packaging", "packaging_tags",
                          "brands", "brands_tags", "categories",
                          "categories_tags", "categories_fr", "labels",
                          "labels_tags", "labels_fr", "purchase_places",
                          "image_url"]

    # barcode, if it starts with "200" it's a OFF custom code provided
    # and barcode is not known yet
    code = fields.StringField(required=True)
    url_OFF = fields.StringField()
    product_name = fields.StringField(required=True)
    generic_name = fields.StringField()
    quantity = fields.StringField()

    packaging = fields.StringField()  # shape, material
    packaging_tags = fields.StringField()
    brands = fields.StringField()
    brands_tags = fields.StringField()
    categories = fields.StringField()
    categories_tags = fields.StringField()
    categories_fr = fields.StringField()
    labels = fields.StringField()
    labels_tags = fields.StringField()
    labels_fr = fields.StringField()
    purchase_places = fields.StringField()
    image_url = fields.StringField()

    def copy(self):
        """
        Dump all fields
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
