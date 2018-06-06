from flask import Blueprint, jsonify

from src.common.decorator import crossdomain
from src.common.errors import CommonErrors
from .constants import *
from .driver import Driver
from .errors import DriverError

Driver_blueprint = Blueprint('driver', __name__)


@Driver_blueprint.route('/login', methods=['POST', 'OPTIONS'])
@crossdomain(origin='http://localhost:8100')
def login():
    try:
        token = Driver.login()
        return jsonify({'Status': 'Accept', 'Token': token})
    except (DriverError, CommonErrors) as e:
        print(e.message)
        return jsonify({'Status': 'Reject'})


@Driver_blueprint.route('/coordination', methods=['POST', 'OPTIONS'])
@crossdomain(origin='http://localhost:8100')
def driver_coordination():  # here we have to update the place of the current driver
    try:
        Driver.update_coordination()
        return jsonify({'Status': 'Accept'})
    except (DriverError, CommonErrors) as e:
        print(e.message)
        return jsonify({'Status': 'Reject', 'message': e.message})


@Driver_blueprint.route('/logout', methods=['POST', 'OPTIONS'])
@crossdomain(origin='http://localhost:8100')
def logout():
    try:
        Driver.logout()
    except (DriverError, CommonErrors) as e:
        print(e.message)
    return jsonify({'Status': 'Accept'})


@Driver_blueprint.route('/forget-password', methods=['POST', 'OPTIONS'])
@crossdomain(origin='http://localhost:8100')
def forget_password():
    try:
        name = Driver.forget_password()
        return jsonify(
            {'Status': 'Accept', 'Duration': CODE_NUMBER_DURATION, 'Length': FORGET_PASSWORD_CODE_LENGTH, 'Name': name})
    except (DriverError, CommonErrors) as e:
        print(e.message)
        return jsonify({'Status': 'Reject'})


@Driver_blueprint.route('/change-password', methods=['POST', 'OPTIONS'])
@crossdomain(origin='http://localhost:8100')
def change_password():
    try:
        Driver.change_password()
        return jsonify({'Status': 'Accept'})
    except (DriverError, CommonErrors) as e:
        print(e.message)
        return jsonify({'Status': 'Reject'})


@Driver_blueprint.route('/check-code-number', methods=['POST', 'OPTIONS'])
@crossdomain(origin='http://localhost:8100')
def check_code_number():
    try:
        token = Driver.check_code_number_validation()
        return jsonify({'Status': 'Accept', "Token": token})
    except (DriverError, CommonErrors) as e:
        print(e.message)
        return jsonify({'Status': 'Reject'})
