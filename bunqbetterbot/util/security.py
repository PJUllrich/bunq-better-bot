import bcrypt
import hashlib
import os
from Cryptodome.Cipher import AES

import util.decorators as deco

_ROUNDS = 12
_KEY_LENGTH = 32  # Results in AES-256
_AES_MODE = AES.MODE_GCM


@deco.ensure_bytes
def derivate_key(key, salt=None):
    if salt is None:
        salt = bcrypt.gensalt(_ROUNDS)

    return bcrypt.hashpw(key, salt)


@deco.ensure_bytes
def hash_key(key):
    return hashlib.blake2b(key, digest_size=_KEY_LENGTH)


@deco.ensure_bytes
def hash_password(pw):
    pw_derivated = derivate_key(pw)
    pw_hashed = hash_key(pw_derivated).hexdigest()
    return pw_hashed


def check_password(pw, salt, hashed):
    return hash_password(pw, salt) == hashed


def encrypt(text_plain, key):
    pp_256 = hash_key(key).digest()
    iv = os.urandom(16)

    cipher = AES.new(pp_256, _AES_MODE, iv)
    text_encrypted = cipher.encrypt(text_plain)

    return text_encrypted, iv


def decrypt(text_encrypted, key, iv):
    pp_256 = hash_key(key).digest()

    cipher = AES.new(pp_256, _AES_MODE, iv)
    text_plain = cipher.decrypt(text_encrypted)

    return text_plain


def create_random_key():
    return os.urandom(_KEY_LENGTH)
