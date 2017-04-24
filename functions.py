from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from Config_Controller import Config
from apiwrapper import API
from pprint import pprint


c = Config('BunqAPI')


def create_new_key_pair():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )

    private_key_decoded = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    ).decode()

    public_key_decoded = private_key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ).decode()

    c.set('KEY_PRIVATE', private_key_decoded)
    c.set('KEY_PUBLIC', public_key_decoded)
    c.save()


def register_key():
    private_key = c.get('KEY_PRIVATE')

    bunq_api = API(private_key, None)

    # using the pubkey() helper function to get public part of key pair
    public_key = bunq_api.pubkey().decode()

    # you will most probably want to store the token that is returned
    r = bunq_api.query('installation', {'client_public_key': public_key})
    token = r.json()['Response'][1]['Token']['token']
    c.set('token', token)
    c.save()
