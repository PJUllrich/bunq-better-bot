import base64

import bcrypt
import hashlib
import os
from Cryptodome.Cipher import AES

_ROUNDS = 11
_KEY_LENGTH = 32  # Results in AES-256
_AES_MODE = AES.MODE_GCM


class KeyEncrypted:
    def __init__(self, key_encrypted, iv):
        self.encrypted_key = key_encrypted
        self.iv = iv

    @property
    def key_encypted_bytes(self):
        return base64.b64decode(self.encrypted_key)

    @property
    def iv_bytes(self):
        return base64.b64decode(self.iv)


def derivate_key(key):
    return bcrypt.hashpw(key, bcrypt.gensalt(_ROUNDS))


def hash_key(key):
    return hashlib.blake2b(key, digest_size=_KEY_LENGTH)


def check_password(pw, hashed):
    pw_derivated = derivate_key(pw)
    pw_hashed = hash_key(pw_derivated).hexdigest()
    return pw_hashed == hashed


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
