from scripts.functions import *

# First, we will create a new key pair (public/private) and save them to the lib/config.ini file
create_new_key_pair()

# Second, we register the key pair at the Bunq API
# Ref: https://doc.bunq.com/api/1/call/installation/method/post
register_key_pair()

# Third, we create a new device server (i.e. register a new device)
# Ref: https://doc.bunq.com/api/1/call/device-server/method/post
create_new_device_server()

# Fourth, we create a new session for making calls
# Ref: https://doc.bunq.com/api/1/call/session-server/method/post
create_new_session()

# Fifth, we retrieve and save the ID of the User
# Caveat: If you have multiple users, this will only save the ID of the first user
# Ref: https://doc.bunq.com/api/1/call/user-person/method/get
get_user_id()

