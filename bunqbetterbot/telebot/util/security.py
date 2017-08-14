import base64
import hashlib

import util.decorators as deco

_KEY_LENGTH = 32  # Results in a 256bit key


def hash_key(key):
    res = hashlib.blake2b(key, digest_size=_KEY_LENGTH).digest()
    return base64.b64encode(res)
