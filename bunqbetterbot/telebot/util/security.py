import hashlib

_KEY_LENGTH = 32  # Results in a 256bit key


def hash_key(key):
    return hashlib.blake2b(key.encode(), digest_size=_KEY_LENGTH).hexdigest()
