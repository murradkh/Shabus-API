import datetime
import uuid

from flask import request

from src.common.database import Database
from src.common.errors import DBErrors
from src.common.utilites import Utils
from src.models.user.driver.driver import Driver
from .constants import *
from .errors import *


class Passenger(object):

    def __init__(self):
        pass

    # @staticmethod
    # def check_json_isvaild():
    #     try:
    #         content = request.get_json()
    #         token = content['Token']
    #         phone_number = content['PhoneNumber']
    #         number_of_passengers = content['Num of passengers']
    #         return token, phone_number, number_of_passengers
    #     except:
    #         raise JsonInValid('The Json file is not valid!')

    @staticmethod
    def new_ride():
        token, phone_number, number_of_passengers = Utils.check_json_vaild(request.get_json(), "Token", "PhoneNumber",
                                                                           "Num of passengers")
        Utils.phone_number_Isvalid(phone_number)
        Passenger.check_num_of_passengers(number_of_passengers)
        passenger_details = Passenger.find_passenger(query={'phone_number': phone_number})
        passenger_details['Number of passengers'] = number_of_passengers
        passenger_details['_id'] = uuid.uuid4().hex
        decoded_token = Utils.decode_token(token=token)
        passenger_details['Wًith driver'] = decoded_token['Name']
        passenger_details['Riding place'] = \
            Driver.get_coordination({'Email': decoded_token['Email']}, {'Current location': 1, '_id': 0})[
                'Current location']  # important thing i did here, its telling the mongo database to give me just the one field without other fields in document(which satisfy the requirements)
        passenger_details['Riding time'] = datetime.datetime.now().strftime("%Y/%m/%d, %H:%M")
        passenger_details['created_at'] = datetime.datetime.now()
        Passenger.store_new_ride(passenger_details)
        return passenger_details['name']

    @staticmethod
    def check_num_of_passengers(number_of_passengers):
        if not (0 < number_of_passengers <= Allowed_Number_Of_Passengers):
            raise ViolationNumberOfPassengers('max passengers allowed is {}'.format(Allowed_Number_Of_Passengers))
        return True

    @staticmethod
    def find_passenger(query):
        try:
            return Database.find_one(collection=DB_collection_Passengers, query=query)
        except DBErrors:
            raise PassengerNotExistError('Not user')

    @staticmethod
    def store_new_ride(query):
        Database.save_to_db(collection=DB_collection_New_Ride, query=query)
