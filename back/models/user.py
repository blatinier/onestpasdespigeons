import time
from mongoengine import Document, fields

from lib.auth import generate_token


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

    def save(self):
        """
        Tweak `save` to delete expired tokens on each save operation
        """
        to_del = []
        now = int(time.time())
        for access_token, clients in self.tokens.items():
            for client, expiry in clients.items():
                if expiry < now:
                    to_del.append((access_token, client))
        for token in to_del:
            self._invalidate_token(*token)
        super().save()
