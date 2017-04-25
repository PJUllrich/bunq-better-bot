from scripts.functions import *

# First, we will create a new key pair (public/private) and save them to the lib/config.ini file
create_new_key_pair()

# Second, we register the key pair at the Bunq API
register_key_pair()

create_new_device_server()

create_new_session()

set_user_id()

get_user_balances()


