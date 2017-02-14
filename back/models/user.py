from mongoengine import Document, fields


# TODO SSO (fb, google au moins, cf jarr)
# TODO field validation
class User(Document):
    meta = {
        'collection': 'users',
        'indexes': [
            'name',
            'email',
        ],
    }

    name = fields.StringField(required=True)
    email = fields.StringField(required=True)
    provider = fields.StringField(required=True, defaut="email")
    password = fields.StringField(required=True)
    role = fields.StringField(required=True)

    # Contains access tokens by clients
    tokens = fields.DictField()

    # TODO delete expired tokens on each save
