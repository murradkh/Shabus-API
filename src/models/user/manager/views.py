from flask import Blueprint, jsonify

from src.common.decorator import crossdomain
from src.common.errors import CommonErrors
from src.models.user.manager.errors import ManagerError
from .manager import Manager

manager_blueprint = Blueprint('manager', __name__)


@manager_blueprint.route('/login', methods=['POST', 'OPTIONS'])
@crossdomain(origin='http://localhost:4200')
def login():
    try:
        token, image = Manager.login()
        return jsonify({'Status': 'Accept', 'Token': token, "Image": image.read().decode()})
    except (ManagerError, CommonErrors) as e:
        print(e.message)
        return jsonify({'Status': 'Reject'})
