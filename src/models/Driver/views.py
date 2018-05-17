from flask import Blueprint, jsonify

from src.models.Driver.decorator import crossdomain
from .driver import Driver
from .errors import Driver_Error

Driver_blueprint = Blueprint('Driver', __name__)


@Driver_blueprint.route('/Driver-login', methods=['POST', 'OPTIONS'])
@crossdomain(origin='http://localhost:8100')
def driver_login():
    try:

        token = Driver.login()
        return jsonify({'Status': 'Accept', 'Token': token})

    except Driver_Error as e:
        print(e.message)
        return jsonify({'Status':'Reject', 'message': 'The login failed, your email/password Incorrect'})





# session['_id'] = driver_details['_id']  # setting the cookie
#   session.permanent = True  # enables the expiration timeout
#   return session['_id']
