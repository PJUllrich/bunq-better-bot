import inspect
import json


def decode_json(func):
    def inner(data_json):
        data_dict = json.loads(data_json)
        return func(data_dict)

    return inner


def decode_dict(func):
    params = inspect.signature(func).parameters.keys()

    def inner(data):
        args = [data.get(p) for p in params]

        if None in args:
            raise ValueError('Not all necessary data was passed.')

        return func(*args)

    return inner


def ensure_byte_input(func):
    def inner(*args):
        data = [e.encode() if not isinstance(e, bytes) else e for e in args]

        return func(*data)

    return inner
