from flask import Blueprint, jsonify, request

from src.common.decorator import crossdomain
from src.common.errors import CommonErrors
from .constants import *
from .driver import Driver
from .errors import DriverError

Driver_blueprint = Blueprint('driver', __name__)


@Driver_blueprint.route('/login', methods=['POST', 'OPTIONS'])
def login():
    if request.method == 'OPTIONS':
        return 'ok'
    try:
        token, image = Driver.login()
        return jsonify({'Status': 'Accept', 'Token': token, "Image": image.read().decode()})
    except (DriverError, CommonErrors) as e:
        print(e.message)
        return jsonify({'Status': 'Reject'})


@Driver_blueprint.route('/coordination', methods=['POST', 'OPTIONS'])
def driver_coordination():  # here we have to update the place of the current driver
    if request.method == 'OPTIONS':
        return 'ok'
    try:
        Driver.update_coordination()
        return jsonify({'Status': 'Accept'})
    except (DriverError, CommonErrors) as e:
        print(e.message)
        return jsonify({'Status': 'Reject', 'message': e.message})


@Driver_blueprint.route('/logout', methods=['POST', 'OPTIONS'])
def logout():
    if request.method == 'OPTIONS':
        return 'ok'
    try:
        Driver.logout()
    except (DriverError, CommonErrors) as e:
        print(e.message)
    return jsonify({'Status': 'Accept'})


@Driver_blueprint.route('/forget-password', methods=['POST', 'OPTIONS'])
@crossdomain(origin="http://localhost:8100/")
def forget_password():
    if request.method == 'OPTIONS':
        return 'ok'
    try:
        token, image = Driver.forget_password()
        return jsonify(
            {'Status': 'Accept', 'Duration': CODE_NUMBER_DURATION, 'CodeLength': FORGET_PASSWORD_CODE_LENGTH,
             'Image': image.read().decode(),
             'Token': token})
    except (DriverError, CommonErrors) as e:
        print(e.message)
        return jsonify({'Status': 'Reject'})


@Driver_blueprint.route('/change-password', methods=['POST', 'OPTIONS'])
def change_password():
    if request.method == 'OPTIONS':
        return 'ok'
    try:
        Driver.change_password()
        return jsonify({'Status': 'Accept'})
    except (DriverError, CommonErrors) as e:
        print(e.message)
        return jsonify({'Status': 'Reject'})


@Driver_blueprint.route('/check-code-number', methods=['POST', 'OPTIONS'])
def check_code_number():
    if request.method == 'OPTIONS':
        return 'ok'
    try:
        token = Driver.check_code_number_validation()
        return jsonify({'Status': 'Accept', "Token": token, 'PasswordMinLength': PASSWORD_MIN_LENGTH})
    except (DriverError, CommonErrors) as e:
        print(e.message)
        return jsonify({'Status': 'Reject'})


@Driver_blueprint.route('/registration', methods=['POST', 'OPTIONS'])
def registration():
    if request.method == 'OPTIONS':
        return 'ok'
    try:
        Driver.registration()
        return jsonify({'Status': 'Accept'})
    except (DriverError, CommonErrors) as e:
        print(e.message)
        return jsonify({'Status': 'Reject', "Message": e.message})


@Driver_blueprint.route('/edit', methods=['POST', 'OPTIONS'])
def edit_details():
    if request.method == 'OPTIONS':
        return 'ok'
    try:
        token = Driver.edit_details()
        return jsonify({'Status': 'Accept', 'Token': token})
    except (DriverError, CommonErrors) as e:
        print(e.message)
        return jsonify({'Status': 'Reject', "Message": e.message})


@Driver_blueprint.route('/confirmation', methods=['POST', 'OPTIONS'])
def confirmation():
    if request.method == 'OPTIONS':
        return 'ok'
    try:
        name = Driver.confirmation_of_driver_account()
        return jsonify({'Status': 'Accept', 'Name': name})
    except (DriverError, CommonErrors) as e:
        print(e.message)
        return jsonify({'Status': 'Reject'})
