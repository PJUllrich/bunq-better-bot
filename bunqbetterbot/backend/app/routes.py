from flask import request, session

import util.decorators as deco
from logic.account import AccountLogic
from logic.budget import BudgetLogic
from run_backend import backend


@backend.before_request
def make_session_permanent():
    session.permanent = True


@backend.route('/user/register', methods=['POST'])
def register():
    return AccountLogic.register(request.data)


@backend.route('/user/login', methods=['POST'])
def login():
    return AccountLogic.login(request.data)


@backend.route('/budget', methods=['GET'])
@deco.require_token
def get_budgets():
    return BudgetLogic.get_updates()


@backend.route('/budget', methods=['POST'])
@deco.require_token
def create_budget():
    return BudgetLogic.create(request.data)
