from flask import session, request

import util.decorators as deco
from logic import account, budget
from run_backend import backend


@backend.before_request
def make_session_permanent():
    session.permanent = True


@backend.route('/user/register', methods=['POST'])
def register():
    return account.register(request.data)


@backend.route('/user/login', methods=['POST'])
def login():
    return account.login(request.data)


@backend.route('/budget', methods=['GET'])
@deco.require_token
def get_budgets():
    return budget.get_updates()


@backend.route('/budget', methods=['POST'])
@deco.require_token
def create_budget():
    return budget.create(request.data)


@backend.route('/')
def hello():
    return 'Hello World'
