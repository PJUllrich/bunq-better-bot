from datetime import datetime

from model import User, UserSession

from backend import util as deco
from backend.util import security


@deco.decode_json
@deco.decode_dict
def register(env, chat_id, pw, key_api):
    user_new = User(env, chat_id, pw, key_api)
    return User.add_user(user_new)


@deco.decode_json
@deco.decode_dict
def login(chat_id, pw):
    user = User.qry_chat_id(chat_id)

    if user is None:
        return False

    pw_auth, pw_encrypt = security.derivate_key(pw, user.)

    authenticated = pw == user.password

    if authenticated:
        usersession_new = UserSession(datetime.now())
        user.session = usersession_new
