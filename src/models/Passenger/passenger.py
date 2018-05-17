from flask import request

from .constants import *
from .errors import *
from ...Common.Database import Database
from ...Common.Utilites import Utils


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
            raise Json_InValid('The Json file is not valid!')

    @staticmethod
    def new_ride():
        token, phone_number, number_of_passengers = Passenger.check_json_isvaild()

        if not Utils.Token_Isvalid(token):
            raise Token_Is_InValid('token is not valid!')

        if Utils.phone_number_Isvalid(phone_number) is None:
            raise Format_PhoneNumber_InValid('the format phone number is invalid!')

        if Passenger.check_num_of_passengers(number_of_passengers) is False:
            raise Violation_number_of_passengers('max passengers allowed is {}'.format(Allowed_Number_Of_Passengers))

        passenger_details = Passenger.find_passenger(query={'phone_number': phone_number})
        if passenger_details is None:
            raise Passenger_NotExist_Error('Not User')
        else:
            Passenger.store_new_ride(passenger_details)
            return passenger_details['name']

    @staticmethod
    def check_num_of_passengers(number_of_passengers):
        if 0 < number_of_passengers <= Allowed_Number_Of_Passengers:
            return True
        return False

    @staticmethod
    def find_passenger(query):
        return Database.find_one(collection=Passengers_Collection, query=query)

    @staticmethod
    def store_new_ride(query):
        pass
        # Database.save_to_DB(collection=New_Ride_Collection,query)

    def save_to_db(self):
        pass

    def json(self):
        pass
