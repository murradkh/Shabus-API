import datetime
import uuid

from flask import request

from src.common.database import Database
from src.common.utilites import Utils
from src.models.user.driver.driver import Driver
from .constants import *
from .errors import *


class Passenger(object):

    def __init__(self):
        pass

    @staticmethod
    def check_json_isvaild():
        try:
            content = request.get_json()
            token = content['Token']
            phone_number = content['Phone_Number']
            number_of_passengers = content['Num_Of_Passengers']
            return token, phone_number, number_of_passengers
        except:
            raise JsonInValid('The Json file is not valid!')

    @staticmethod
    def new_ride():
        token, phone_number, number_of_passengers = Passenger.check_json_isvaild()

        if not Utils.Token_Isvalid(token):
            raise TokenIsInValid('token is not valid!')

        if Utils.phone_number_Isvalid(phone_number) is None:
            raise FormatPhoneNumberInValid('the format phone number is invalid!')

        if Passenger.check_num_of_passengers(number_of_passengers) is False:
            raise ViolationNumberOfPassengers('max passengers allowed is {}'.format(Allowed_Number_Of_Passengers))

        passenger_details = Passenger.find_passenger(query={'phone_number': phone_number})
        if passenger_details is None:
            raise PassengerNotExistError('Not user')
        else:
            passenger_details['Number Of Passegers'] = number_of_passengers
            passenger_details['_id'] = uuid.uuid4().hex
            decoded_token = Utils.decode_token(token=token)
            passenger_details['Wًith Driver'] = decoded_token['email']
            passenger_details['Riding Place'] = \
            Driver.get_coordination({'email': decoded_token['email']}, {'coordination': 1, '_id': 0})[
                'coordination']  # important thing i did here, its telling the mongo database to give me just the one field without other fields in document(which satisfy the requirements)
            passenger_details['Riding Time'] = datetime.datetime.now().strftime("%Y/%m/%d, %H:%M")
            Passenger.store_new_ride(passenger_details)
            return passenger_details.get('name') if passenger_details.get('name') is not None else ""

    @staticmethod
    def check_num_of_passengers(number_of_passengers):
        if 0 < number_of_passengers <= Allowed_Number_Of_Passengers:
            return True
        return False

    @staticmethod
    def find_passenger(query):
        return Database.find_one(collection=DB_collection_Passengers, query=query)

    @staticmethod
    def store_new_ride(query):
        Database.save_to_db(collection=DB_collection_New_Ride, query=query)
