"""
DISCLAIMER: This code was mostly taken from the example files in https://github.com/madeddie/python-bunq
Thanks for @madeddie for writing these examples and the API Wrapper
"""

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

from lib.apiwrapper import API
from lib.config.controller import Controller

config = Controller()


def create_new_key_pair():
    """Creates a new public/private key pair and saves them to the config file
    
    :return: Prints out a success message
    """
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

    config.set('KEY_PRIVATE', private_key_decoded)
    config.set('KEY_PUBLIC', public_key_decoded)

    print('New key pair created and saved to config.ini file.')


def register_key_pair():
    """Registers a public/private key pair with the Bunq API
    Ref: https://doc.bunq.com/api/1/call/installation/method/post
    
    Saves the installation (user) token and server public key to config
    
    KEY_PRIVATE needs to be set in the config for this method to run
    
    :return: Prints out either a success message or the Error message of the API
    """
    private_key = config.get('KEY_PRIVATE')
    bunq_api = API(private_key, None)
    public_key = bunq_api.pubkey().decode()

    r = bunq_api.query('installation', {'client_public_key': public_key})
    if r.status_code == 200:
        token_entry = [x for x in r.json()['Response'] if list(x)[0] == 'Token'][0]
        server_entry = [x for x in r.json()['Response'] if list(x)[0] == 'ServerPublicKey'][0]

        token_user = token_entry['Token']['token']
        server_public_key = server_entry['ServerPublicKey']['server_public_key']

        config.set('TOKEN_USER', token_user)
        config.set('SERVER_PUBLIC_KEY', server_public_key)

        print('Key pair was registered successfully.')
    else:
        print('Register Key Pair Error: ' + r.json()['Error'][0])


def create_new_device_server():
    """Creates a new device server at the Bunq API 
    Ref: https://doc.bunq.com/api/1/call/device-server/method/post
    
    API_KEY needs to be set in the config for this method to run
    
    :return: Prints out either a success message or the Error message of the API
    """
    api_key = config.get('API_KEY')
    bunq_api = get_api_connection(False)

    r = bunq_api.query('device-server', {'description': 'Peter MacBook Pro', 'secret': api_key})
    if r.status_code == 200:
        print('New device server was created successfully.')
    else:
        print('Create Session Error: ' + str(r.json()['Error'][0]))


def create_new_session():
    """Creates a new session at the Bunq API
    Ref: https://doc.bunq.com/api/1/call/session-server/method/post
    
    Saves the session token to config
    
    API_KEY needs to be set in the config for this method to run
    
    :return: Prints out either a success message or the Error message of the API
    """
    bunq_api = get_api_connection(False)
    api_key = config.get('API_KEY')

    r = bunq_api.query('session-server', {'secret': api_key})
    if r.status_code == 200:
        res = [x for x in r.json()['Response'] if list(x)[0] == 'Token'][0]
        session_token = res['Token']['token']
        config.set('TOKEN_SESSION', session_token)
        print('New session was created successfully.')
    else:
        print('Create Session Error: ' + str(r.json()['Error'][0]))


def get_user_id():
    """Retrieves the id of the first user of an accounts from the Bunq API
    Saves the id to config
    
    :return: Prints out either a success message or the Error message of the API
    """
    bunq_api = get_api_connection()
    r = bunq_api.query('user', verify=True)
    if r.status_code == 200:
        res = [x for x in r.json()['Response'] if list(x)[0] == 'UserPerson'][0]
        user_id = res['UserPerson']['id']
        config.set('USER_ID', str(user_id))
        print('User id retrieved successfully.')
    else:
        print('Retrieve User ID Error: ' + str(r.json()['Error'][0]))


def get_api_connection(with_token_session=True):
    """Creates an instance of the API class in apiwrapper with info from the config
    
    TOKEN_USER, KEY_PRIVATE, and SERVER_PUBLIC_KEY need to be set in order for this method to run
    Optional:   The session token can be added to the API object. 
                For this TOKEN_SESSION needs to be set in config.
    
    :param with_token_session: Boolean. Add session token to API object.
    :return: An object of the API class in apiwrapper. w
    """
    token = config.get('TOKEN_USER')
    private_key = config.get('KEY_PRIVATE')
    server_public_key = config.get('SERVER_PUBLIC_KEY')

    connection = API(private_key, token, servkey_pem=server_public_key)
    if with_token_session:
        connection.token = config.get('TOKEN_SESSION')

    return connection

