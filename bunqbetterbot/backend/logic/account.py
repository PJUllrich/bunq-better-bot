import logging

from flask import session, jsonify

import util.decorators as deco
from app import const
from model import Key, User
from util import security

logger = logging.getLogger(__name__)


@deco.decode_from_json
def register(env, chat_id, pw, key_api):
    logger.info('Received new register request')

    user = User.qry_by('chat_id', chat_id).first()

    if user is not None:
        return 'User does exist already!', 403

    pws, salt_pw = security.derivate_key(pw, None, num_keys=2)

    pw_auth = pws[0]
    pw_encrypt = pws[1]

    key_api_encrypted, salt_api = security.encrypt(key_api, pw_encrypt)

    key_auth = Key(pw_auth, salt_pw)
    key_api = Key(key_api_encrypted, salt_api)

    user_new = User(env, chat_id, key_auth, key_api)

    try:
        User.add(user_new)
        return 'Account created', 201
    except Exception as e:
        return False, str(e)


@deco.decode_from_json
def login(chat_id, pw):
    user = User.qry_by('chat_id', chat_id).first()

    if user is None:
        return 'Either account non-existent or password incorrect', 401

    pws, _ = security.derivate_key(pw, user.key_auth.salt, num_keys=2)

    if pws[0] != user.key_auth.value:
        return 'Either account non-existent or password incorrect', 401

    token = security.gen_token()
    api_key = security.decrypt(user.key_api.value, pws[1], user.key_api.salt)

    session[const.USER_ID] = user.id
    session[const.AUTH_TOKEN] = token
    session[const.API_KEY] = api_key

    return jsonify({const.AUTH_TOKEN: token}), 200
