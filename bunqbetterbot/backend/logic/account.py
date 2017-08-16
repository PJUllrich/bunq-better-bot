import logging

from flask import jsonify, session

import util.decorators as deco
import bunq.sdk.model.generated.endpoint as bunq
from app import const, errors
from bunq.sdk.context import ApiContext, ApiEnvironmentType
from model import EncryptedData, User
from util import security

logger = logging.getLogger(__name__)


class AccountLogic:
    @classmethod
    @deco.decode_from_json
    def register(cls, env, chat_id, pw, api_key):
        logger.info('Received new register request')

        user_exists = AccountLogic._check_user_exists(chat_id)
        if user_exists:
            return errors.USER_EXISTS, 403

        api_env = cls._get_api_env(env.upper())
        api_conf = cls._get_api_conf(api_env, api_key)

        pws, salt_pw = security.derivate_key(pw, num_keys=2)
        pw_auth, pw_encrypt = cls._get_passwords(pws)

        api_conf_encrypted, salt_api = security.encrypt(api_conf, pw_encrypt)

        auth_data = EncryptedData(pw_auth, salt_pw)
        api_data = EncryptedData(api_conf_encrypted, salt_api)

        user_new = User(chat_id, auth_data, api_data)

        try:
            User.add(user_new)
            return 'Account created', 201
        except Exception as e:
            return str(e), 500

    @staticmethod
    @deco.decode_from_json
    def login(chat_id, pw):
        user = User.qry_by('chat_id', chat_id).first()

        if user is None:
            return errors.PW_INCORRECT_OR_NO_ACCOUNT, 401

        pws, _ = security.derivate_key(pw, user.auth.salt, num_keys=2)

        if pws[0] != user.auth.value:
            return errors.PW_INCORRECT_OR_NO_ACCOUNT, 401

        token = security.gen_token()
        api_conf = security.decrypt(user.api_conf.value, pws[1], user.api_conf.salt)

        session[const.AUTH_TOKEN] = token
        session[const.API_CONF] = api_conf

        return jsonify({const.AUTH_TOKEN: token}), 200

    @classmethod
    @deco.decode_from_json
    def list_active_accounts(cls, auth_token):
        api_conf = session[const.API_CONF]
        api_context = ApiContext.from_json(api_conf)

        user_info = bunq.User.list(api_context)
        print(user_info)



    @classmethod
    def _check_user_exists(cls, chat_id):
        return cls._get_user(chat_id) is not None

    @staticmethod
    def _get_passwords(pws):
        pw_auth = pws[0]
        pw_encrypt = pws[1]
        return pw_auth, pw_encrypt

    @staticmethod
    def _get_user(chat_id):
        return User.qry_by('chat_id', chat_id).first()

    @staticmethod
    def _get_api_env(env):
        if env == 'SANDBOX':
            return ApiEnvironmentType.SANDBOX
        else:
            return ApiEnvironmentType.PRODUCTION

    @classmethod
    def _get_api_conf(cls, api_env, api_key):
        return cls._create_api_context(api_env, api_key).to_json()

    @staticmethod
    def _create_api_context(api_env, api_key):
        return ApiContext(api_env, api_key, const.DEVICE_DESCRIPTION)
