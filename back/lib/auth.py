import hashlib
import time
import uuid

import config.main as conf


def hashfunc(string):
    return hashlib.sha256(string).hexdigest()


def generate_token(client=None):
    return {"access-token": str(uuid.uuid4()),
            "token-type": "Bearer",
            "expiry": int(time.time()) + conf.TOKEN_LIFESPAN,
            "client": client or str(uuid.uuid4())}


def validate_new_password(pwd, pwd_confirmation):
    return pwd == pwd_confirmation
