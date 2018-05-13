from flask import Blueprint, jsonify

from .errors import Passenger_Error
from .passenger import Passenger

passenger_blueprint = Blueprint('passenger', __name__)


@passenger_blueprint.route('/Passenger-New-Ride', methods=['OPTIONS', 'POST'])
def New_Ride_For_Passenger():
    try:

        Passenger.New_Ride()
        return jsonify({'Status': 'Accept'})

    except Passenger_Error as e:
        print(e.message)
        return jsonify({'Status': 'Reject', 'message': 'something goes wrong! please try again.'})
