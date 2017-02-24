import time
from mongoengine import Document, fields
from mongoengine import signals as mongoengine_signals

from lib.auth import generate_token


class User(Document):
    meta = {
        'collection': 'users',
        'indexes': [
            'name',
            'email',
            'login'
        ],
    }

    name = fields.StringField(required=True)
    email = fields.StringField(required=True)
    login = fields.StringField(required=True)
    provider = fields.StringField(required=True, defaut="email")
    password = fields.StringField(required=True)
    role = fields.StringField(required=True)

    # Contains access tokens by clients
    tokens = fields.DictField()

    def is_token_valid(self, access_token, client):
        now = int(time.time())
        return (access_token in self.tokens and
                client in self.tokens[access_token] and
                self.tokens[access_token][client] < now)

    def _invalidate_token(self, access_token, client):
        del self.tokens[access_token][client]

    def invalidate_token(self, access_token, client):
        del self.tokens[access_token][client]
        self.save()

    def generate_token(self, client=None):
        token = generate_token(client)
        self.tokens[token["access-token"]] = {token["client"]: token["expiry"]}
        self.save()
        token.update({"uid": self._id})
        return token

    def dump(self):
        return {"uid": self._id,
                "provider": self.provider,
                "name": self.name,
                "email": self.email,
                "login": self.login,
                "role": self.role}

    @classmethod
    def pre_save(cls, sender, document, **kwargs):
        """
        Delete expired tokens on each save operation.
        Hooked on pre_save mongoengine signal (see end of file)
        """
        to_del = []
        now = int(time.time())
        for access_token, clients in document.tokens.items():
            for client, expiry in clients.items():
                if expiry < now:
                    to_del.append((access_token, client))
        for token in to_del:
            document._invalidate_token(*token)


mongoengine_signals.pre_save.connect(User.pre_save, sender=User)
