import base64
import hashlib
import os
import struct

from Cryptodome.Cipher import AES
from Cryptodome.Protocol.KDF import scrypt

KEY_LENGTH = 32  # Results in a 256bit key

# Decision based on https://www.owasp.org/index.php?title=Password_Storage_Cheat_Sheet
_SALT_LENGTH = 32

# Decision based on http://www.tarsnap.com/scrypt/scrypt-slides.pdf
# Documentation: https://legrandin.github.io/pycryptodome/Doc/3.2/Crypto.Protocol.KDF-module.html
_COST_FACTOR = 14
_BLOCK_SIZE = 8
_PARAM_PARALLELIZATION = 1

_AES_MODE = AES.MODE_GCM


def derivate_key(key, salt=None, num_keys=1):
    if salt is None:
        salt = gen_token()

    key, salt = to_bytes(key), to_bytes(salt)

    key_hashed = scrypt(key, salt, KEY_LENGTH,
                        2 ** _COST_FACTOR,
                        _BLOCK_SIZE,
                        _PARAM_PARALLELIZATION,
                        num_keys)

    if num_keys > 1:
        key_hashed = [to_str(k) for k in key_hashed]
    else:
        key_hashed = to_str(key_hashed)

    salt = to_str(salt)

    return key_hashed, salt


def hash_key(key):
    key = to_bytes(key)
    res = hashlib.blake2b(key, digest_size=KEY_LENGTH).digest()
    return to_str(res)


def gen_token():
    return to_str(os.urandom(KEY_LENGTH))


def encrypt(text_plain, key):
    text_plain, key = to_bytes(text_plain), to_bytes(key)
    iv = base64.b64encode(os.urandom(_SALT_LENGTH))

    cipher = AES.new(key, _AES_MODE, iv)
    ciphertext = cipher.encrypt(text_plain)

    return to_str(ciphertext), to_str(iv)


def decrypt(ciphertext, key, iv):
    ciphertext, key, iv = to_bytes(ciphertext), to_bytes(key), to_bytes(iv)

    cipher = AES.new(key, _AES_MODE, iv)
    text_plain = cipher.decrypt(ciphertext)

    return to_str(text_plain)


def to_str(val):
    if val is None or isinstance(val, str):
        return val

    return base64.b64encode(val).decode()


def to_bytes(val):
    if val is None or isinstance(val, bytes):
        return val

    if isinstance(val, str):
        # try:
            return base64.b64encode(val)
        # except base64.binascii.Error:
            # return to_bytes(base64.b64encode(val).decode())

    if isinstance(val, int):
        return base64.b64decode(str(val))

    if isinstance(val, float):
        return bytearray(struct.pack("f", val))
