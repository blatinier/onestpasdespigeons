import hashlib
import uuid

from mongoengine import Document, fields


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
    role = fields.StringField(required=True)
    password = fields.StringField(required=True)
    session_token = fields.StringField()

    @staticmethod
    def hash_password(pwd):
        return hashlib.sha1(pwd).hexdigest()

    @staticmethod
    def log_in(email, pwd):
        return User.objects.get(email=email,
                                password=User.hash_password(pwd))

    def get_new_token(self):
        self.session_token = str(uuid.uuid4())
        self.save()
        return self.session_token
