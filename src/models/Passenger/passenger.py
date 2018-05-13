from flask import request

from src.Common.Utilites import Utils
from .errors import Json_InValid, Format_PhoneNumber_InValid, Token_Is_InValid


class Passenger(object):

    def __init__(self):
        pass

    @staticmethod
    def check_json_IsVaild():
        try:
            content = request.get_json()
            token = content['Token']
            phone_number = content['Phone_Number']
            return token, phone_number
        except:
            raise Json_InValid('The Json file is not valid')

    @staticmethod
    def New_Ride():
        token, phone_number = Passenger.New_Ride()
        if not Utils.Token_Isvalid(token):
            raise Token_Is_InValid('token is not valid!')

        if Utils.phone_number_Isvalid(phone_number) is False:
            raise Format_PhoneNumber_InValid('the format the phone number is invalid!')

    @staticmethod
    def find_passenger(query):
        pass

    def save_to_db(self):
        pass

    def json(self):
        pass
