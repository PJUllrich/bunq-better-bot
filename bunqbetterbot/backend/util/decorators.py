import inspect
import json

from flask import jsonify, session
from functools import wraps

from app import const


def jsonify_return(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        res = func(*args, **kwargs)
        return tuple(jsonify(res[0]) + list(res[1:]))

    return wrapper


def decode_from_json(func):
    params = inspect.signature(func).parameters.keys()

    @wraps(func)
    def wrapper(data_json):
        data_dict = json.loads(data_json)
        args = [data_dict.get(p) for p in params]

        if None in args:
            raise ValueError('Not all necessary data was passed.')

        return func(*args)

    return wrapper


def require_token(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if const.AUTH_TOKEN not in session:
            return "Login required", 401

        return func(*args, **kwargs)

    return wrapper
