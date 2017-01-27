from mongoengine import Document, fields

from .product import Product
from .user import User


class Measure(Document):
    meta = {
        'collection': 'measures',
        'indexes': [
            'product',
            'user',
        ],
    }

    product = fields.RefenceField(Product, required=True)
    user = fields.ReferenceField(User, required=True)

    user_measure = fields.DecimalField(require=True)
    # http://stackoverflow.com/questions/13856395/save-imagefield-mongoengine#13856829
    image = fields.ImageField()
