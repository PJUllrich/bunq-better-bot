from datetime import datetime

import util.decorators as deco
from model import User, UserSession


@deco.decode_json
@deco.decode_dict
def register(env, chat_id, password_hash, key_api, key_encrypt):
    user_new = User(env, chat_id, password_hash, key_api, key_encrypt)
    return User.add_user(user_new)


@deco.decode_json
@deco.decode_dict
def login(chat_id, pw_hashed):
    user = User.qry_chat_id(chat_id)

    if user is None:
        return False

    authenticated = pw_hashed == user.password

    if authenticated:
        usersession_new = UserSession(datetime.now())
        user.session = usersession_new
