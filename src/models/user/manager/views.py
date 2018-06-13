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
        token = Manager.login()
        return jsonify({'Status': 'Accept', 'Token': token})
    except (ManagerError, CommonErrors) as e:
        print(e.message)
        return jsonify({'Status': 'Reject'})


@manager_blueprint.route('/<string:param>', methods=['GET', 'OPTIONS'])
@crossdomain(origin='http://localhost:4200')
def get_data(param):
    print(param)
    data = Manager.get_data(collection=param)
    d = {i: x for i, x in enumerate(data)}
    print(d)
    # return 'ok'
    return jsonify({'Status': 'Accept', "Data": d})
#     for i in data:
#         print(i)
#     return jsonify({'Status': 'Accept', "Data": data})
# except (ManagerError, CommonErrors) as e:
#     print(e.message)
#     return jsonify({'Status': 'Reject'})
