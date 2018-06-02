from flask import Blueprint, jsonify

from src.common.decorator import crossdomain
from .driver import Driver
from .errors import DriverError

Driver_blueprint = Blueprint('driver', __name__)


@Driver_blueprint.route('/login', methods=['POST', 'OPTIONS'])
@crossdomain(origin='http://localhost:8100')
def login():
    try:
        token = Driver.login()
        return jsonify({'Status': 'Accept', 'Token': token})
    except DriverError as e:
        print(e.message)
        return jsonify({'Status': 'Reject', 'message': 'The login failed, your email/password Incorrect'})


@Driver_blueprint.route('/coordination', methods=['POST', 'OPTIONS'])
@crossdomain(origin='http://localhost:8100')
def driver_coordination():  # here we have to update the place of the current driver
    try:
        Driver.update_coordination()
        return jsonify({'Status': 'Accept'})
    except DriverError as e:
        print(e)
        return jsonify({'Status': 'Reject', 'message': e.message})


@Driver_blueprint.route('/logout', methods=['POST', 'OPTIONS'])
@crossdomain(origin='http://localhost:8100')
def logout():
    try:
        Driver.logout()
    except DriverError as e:
        print(e.message)
    return jsonify({'Status': 'Accept'})
