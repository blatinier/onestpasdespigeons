import hashlib


def hashfunc(string):
    return hashlib.sha256(string).hexdigest()
