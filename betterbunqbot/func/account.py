import util.decorators as deco
from model import User


@deco.decode_json
@deco.decode_dict
def register(phone, password, key):
    user_new = User(phone, password, key)
    return User.add_user(user_new)


@deco.decode_json
@deco.decode_dict
def login(phone, password):
    return User.login(phone, password)
