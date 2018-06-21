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


@manager_blueprint.route('/Get/<string:param>', methods=['POST', 'OPTIONS'])
def get_data(param):
    if request.method == 'OPTIONS':
        return 'ok'
    try:
        data = Manager.get_data(collection=param)
        return jsonify({'Status': 'Accept', "Data": data})
    except (ManagerError, CommonErrors) as e:
        print(e.message)
        return jsonify({'Status': 'Reject'})


@manager_blueprint.route('/Delete/<string:param>', methods=['POST', 'OPTIONS'])
def delete_data(param):
    if request.method == 'OPTIONS':
        return 'ok'
    try:
        data = Manager.delete(collection=param)
        return jsonify({'Status': 'Accept', "Data": data})
    except (ManagerError, CommonErrors) as e:
        print(e.message)
        return jsonify({'Status': 'Reject'})
