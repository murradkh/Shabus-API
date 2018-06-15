from flask import Blueprint, jsonify, request

from src.common.errors import CommonErrors
from .errors import PassengerError
from .passenger import Passenger

passenger_blueprint = Blueprint('passenger', __name__)


@passenger_blueprint.route('/new-ride', methods=['OPTIONS', 'POST'])
def new_ride():
    if request.method == 'OPTIONS':
        return 'ok'
    try:
        passenger_name = Passenger.new_ride()
        return jsonify({'Status': 'Accept', 'name': passenger_name})

    except (PassengerError, CommonErrors) as e:
        print(e.message)
        return jsonify({'Status': 'Reject', 'message': e.message})
