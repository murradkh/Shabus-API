from flask import Blueprint
from .decorator import valid_token_exist

passenger_blueprint = Blueprint('passenger',__name__)


@passenger_blueprint.route('/Passenger-New-Ride', methods=['OPTIONS', 'POST'])
@valid_token_exist
def New_Ride_For_Passenger():
    pass
