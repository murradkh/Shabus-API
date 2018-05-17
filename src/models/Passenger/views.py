from flask import Blueprint, jsonify

from .decorator import crossdomain
from .errors import Passenger_Error
from .passenger import Passenger

passenger_blueprint = Blueprint('passenger', __name__)


@passenger_blueprint.route('/Passenger-New-Ride', methods=['OPTIONS', 'POST'])
@crossdomain(origin='http://localhost:8100')
def new_ride_for_passenger():
    try:

        passenger_name = Passenger.new_ride()
        return jsonify({'Status': 'Accept', 'name': passenger_name})

    except Passenger_Error as e:
        print(e.message)
        return jsonify({'Status': 'Reject', 'message': e.message})
