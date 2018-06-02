from flask import Blueprint, jsonify

from src.common.decorator import crossdomain
from .errors import PassengerError
from .passenger import Passenger

passenger_blueprint = Blueprint('passenger', __name__)


@passenger_blueprint.route('/new-ride', methods=['OPTIONS', 'POST'])
@crossdomain(origin='http://localhost:8100')
def new_ride():
    try:
        passenger_name = Passenger.new_ride()
        return jsonify({'Status': 'Accept', 'name': passenger_name})

    except PassengerError as e:
        print(e.message)
        return jsonify({'Status': 'Reject', 'message': e.message})
