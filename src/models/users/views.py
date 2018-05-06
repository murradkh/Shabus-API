from datetime import timedelta
from flask import Blueprint, session, redirect, url_for, request, session, make_response
from .Driver import Driver
from .errors import  Driver_Error


Driver_blueprint = Blueprint('Driver', __name__)

@Driver_blueprint.route('/Driver-login', methods=['POST'])
def Driver_login():
    try:
        print(session.get('_id'))
        email, password = Driver.check_Form_vaild() #  checking the form hace valid fields
        driver_details = Driver.check_login_valid(email, password) # checking the user data
        session['_id'] = driver_details['_id'] #  setting the cookie
        session.permanent = True  # enables the expiration timeout
        return ''
    except Driver_Error as e:
        return e.message
