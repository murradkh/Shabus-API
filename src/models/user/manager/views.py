from flask import Blueprint, jsonify, request

from src.common.errors import CommonErrors
from src.models.user.manager.errors import ManagerError
from .manager import Manager

manager_blueprint = Blueprint('manager', __name__)


@manager_blueprint.route('/login', methods=['POST', 'OPTIONS'])
def login():
    if request.method == 'OPTIONS':
        return 'ok'
    try:
        token = Manager.login()
        return jsonify({'Status': 'Accept', 'Token': token})
    except (ManagerError, CommonErrors) as e:
        print(e.message)
        return jsonify({'Status': 'Reject'})


@manager_blueprint.route('/<string:param>', methods=['GET', 'OPTIONS'])
def get_data(param):
    if request.method == 'OPTIONS':
        return 'ok'
    data = Manager.get_data(collection=param)
    d = [x for x in data]
    return jsonify({'Status': 'Accept', "Data": d})
