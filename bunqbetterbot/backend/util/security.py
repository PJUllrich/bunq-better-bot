import hashlib
import os
from Cryptodome.Cipher import AES
from Cryptodome.Protocol.KDF import scrypt

import util.decorators as deco

_KEY_LENGTH = 32  # Results in a 256bit key

# Decision based on https://www.owasp.org/index.php?title=Password_Storage_Cheat_Sheet
_SALT_LENGTH = 32

# Decision based on http://www.tarsnap.com/scrypt/scrypt-slides.pdf
# Documentation: https://legrandin.github.io/pycryptodome/Doc/3.2/Crypto.Protocol.KDF-module.html
_PARAM_COST = 16384
_BLOCK_SIZE = 8
_PARAM_PARALLELIZATION = 1

_AES_MODE = AES.MODE_GCM


@deco.ensure_byte_input
def derivate_key(key, salt=None, num_keys=1):
    if salt is None:
        salt = create_random_key()

    key_hashed = scrypt(key, salt, _KEY_LENGTH,
                        _PARAM_COST,
                        _BLOCK_SIZE,
                        _PARAM_PARALLELIZATION,
                        num_keys)

    return key_hashed, salt


@deco.ensure_byte_input
def hash_key(key):
    return hashlib.blake2b(key, digest_size=_KEY_LENGTH)


@deco.ensure_byte_input
def encrypt(text_plain, key):
    iv = os.urandom(_SALT_LENGTH)

    cipher = AES.new(key, _AES_MODE, iv)
    text_encrypted = cipher.encrypt(text_plain)

    return text_encrypted, iv


@deco.ensure_byte_input
def decrypt(text_encrypted, key, iv):
    cipher = AES.new(key, _AES_MODE, iv)
    text_plain = cipher.decrypt(text_encrypted)

    return text_plain


def create_random_key():
    return os.urandom(_KEY_LENGTH)
