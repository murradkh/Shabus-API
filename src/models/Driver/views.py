from flask import Blueprint, jsonify
from src.models.Driver.decorator import crossdomain
from .driver import Driver
from .errors import Driver_Error
from ...Common.Utilites import Utils

Driver_blueprint = Blueprint('Driver', __name__)


@Driver_blueprint.route('/Driver-login', methods=['POST', 'OPTIONS'])
@crossdomain(origin='http://localhost:8100')
def Driver_login():
    try:

        email, password = Driver.check_Json_vaild()  # checking the json file have valid fields
        driver_details = Driver.check_login_valid(email, password)  # checking the user data is valid with database data
        token = Utils.Create_Token(driver_details['_id'])  # Creating token according to user id(more safer than according the user email)
        return jsonify({'Status': 'Accept', 'Token': token})

    except Driver_Error as e:
        print(e.message)
        return jsonify({'Status':'Reject', 'message': 'The login failed, your email/password Incorrect'})





# session['_id'] = driver_details['_id']  # setting the cookie
#   session.permanent = True  # enables the expiration timeout
#   return session['_id']
