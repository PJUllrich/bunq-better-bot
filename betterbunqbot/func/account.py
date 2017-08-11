import util.decorators as deco
from model import User


@deco.decode_json
@deco.decode_dict
def register(env, chat_id, password_hash, key_api, key_encrypt):
    user_new = User(env, chat_id, password_hash, key_api, key_encrypt)
    return User.add_user(user_new)


@deco.decode_json
@deco.decode_dict
def login(phone, password):
    return User.login(phone, password)
