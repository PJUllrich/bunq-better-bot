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
    params = list(inspect.signature(func).parameters.keys())

    def get_func_args(data_json, keys):
        data_dict = json.loads(data_json)
        return [data_dict.get(p) for p in keys]

    @wraps(func)
    def wrapper(*args):
        if inspect.isclass(args[0]) or params[0] == 'self':
            func_args = get_func_args(args[1], params[1:])
            func_args = [args[0]] + func_args
        else:
            func_args = get_func_args(args[0], params)

        if None in func_args:
            raise ValueError('Not all necessary data was passed.')

        return func(*func_args)

    return wrapper


def require_token(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if const.AUTH_TOKEN not in session:
            return "Login required", 401

        return func(*args, **kwargs)

    return wrapper
