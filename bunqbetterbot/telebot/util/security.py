import hashlib

import util.decorators as deco

_KEY_LENGTH = 32  # Results in a 256bit key


@deco.ensure_byte_input
def hash_key(key):
    return hashlib.blake2b(key, digest_size=_KEY_LENGTH)
