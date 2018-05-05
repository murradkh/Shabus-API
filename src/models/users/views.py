from flask import Blueprint, redirect, url_for, request, session
from src.models.users.constants import COLLECTION
from .Driver import Driver
from .errors import  Driver_Error
Driver_blueprint = Blueprint('Driver', __name__)


@Driver_blueprint.route('/Driver-login', methods=['POST'])
def Driver_login():
    try:

        email, password = Driver.check_Form_vaild()

        Driver.check_login_valid(email, password)
        # add here sending token to the Driver
        return 'token'

    except Driver_Error as e:
        return e.message

    return 'oka'
