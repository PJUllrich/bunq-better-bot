"""
DISCLAIMER: This code was mostly taken from the example files in https://github.com/madeddie/python-bunq
Thanks for @madeddie for writing these examples and the API Wrapper
"""


from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

from lib.Configcontroller import Config
from lib.Apiwrapper import API

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
    print('New key pair created and saved to config.ini file.')


def register_key_pair():
    private_key = c.get('KEY_PRIVATE')
    bunq_api = API(private_key, None)
    public_key = bunq_api.pubkey().decode()

    r = bunq_api.query('installation', {'client_public_key': public_key})
    if r.status_code == 200:
        token_entry = [x for x in r.json()['Response'] if list(x)[0] == 'Token'][0]
        server_entry = [x for x in r.json()['Response'] if list(x)[0] == 'ServerPublicKey'][0]

        token_user = token_entry['Token']['token']
        server_public_key = server_entry['ServerPublicKey']['server_public_key']

        c.set('TOKEN_USER', token_user)
        c.set('SERVER_PUBLIC_KEY', server_public_key)
    else:
        print('Register Key Pair Error: ' + r.json()['Error'][0])


def create_new_device_server():
    api_key = c.get('API_KEY')
    bunq_api = get_api_connection(False)

    r = bunq_api.query('device-server', {'description': 'Peter MacBook Pro', 'secret': api_key})
    if r.status_code == 200:
        print('New device server was created successfully.')
    else:
        print('Create Session Error: ' + str(r.json()['Error'][0]))


def create_new_session():
    bunq_api = get_api_connection(False)
    api_key = c.get('API_KEY')

    r = bunq_api.query('session-server', {'secret': api_key})
    if r.status_code == 200:
        res = [x for x in r.json()['Response'] if list(x)[0] == 'Token'][0]
        session_token = res['Token']['token']
        c.set('TOKEN_SESSION', session_token)
        print('New session was created successfully.')
    else:
        print('Create Session Error: ' + str(r.json()['Error'][0]))


def set_user_id():
    bunq_api = get_api_connection()
    r = bunq_api.query('user', verify=True)
    if r.status_code == 200:
        res = [x for x in r.json()['Response'] if list(x)[0] == 'UserPerson'][0]
        user_id = res['UserPerson']['id']
        c.set('USER_ID', str(user_id))
        print('User id retrieved successfully.')
    else:
        print('Retrieve User ID Error: ' + str(r.json()['Error'][0]))


def get_user_balances():
    bunq_api = get_api_connection()
    user_id = c.get('USER_ID')

    r = bunq_api.query('user/%s/monetary-account-bank' % user_id, verify=True)
    if r.status_code == 200:
        acc_type = 'MonetaryAccountBank'
        res = [x for x in r.json()['Response'] if list(x)[0] == acc_type][0]
        acc = res[acc_type]
        print('%s: %s %s' % (
            acc['description'],
            acc['balance']['value'],
            acc['balance']['currency']
        ))
    else:
        print('Retrieve Account Balances Error: ' + str(r.json()['Error'][0]))


def get_api_connection(with_token_session=True):
    token = c.get('TOKEN_USER')
    private_key = c.get('KEY_PRIVATE')
    server_public_key = c.get('SERVER_PUBLIC_KEY')

    connection = API(private_key, token, servkey_pem=server_public_key)
    if with_token_session:
        connection.token = c.get('TOKEN_SESSION')

    return connection


