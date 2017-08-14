import hashlib
import os

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
        salt = os.urandom(_SALT_LENGTH)

    key_hashed = scrypt(key, salt, KEY_LENGTH,
                        2 ** _COST_FACTOR,
                        _BLOCK_SIZE,
                        _PARAM_PARALLELIZATION,
                        num_keys)

    return key_hashed, salt


def hash_key(key):
    return hashlib.blake2b(key, digest_size=KEY_LENGTH).digest()


def gen_token():
    return hashlib.blake2b(os.urandom(KEY_LENGTH), digest_size=KEY_LENGTH).hexdigest()


def encrypt(text_plain, key):
    text_bytes = text_plain.encode()
    iv = os.urandom(_SALT_LENGTH)

    cipher = AES.new(key, _AES_MODE, iv)
    ciphertext = cipher.encrypt(text_bytes)

    return ciphertext, iv


def decrypt(ciphertext, key, iv):
    cipher = AES.new(key, _AES_MODE, iv)
    text_plain = cipher.decrypt(ciphertext)

    return text_plain.decode()
