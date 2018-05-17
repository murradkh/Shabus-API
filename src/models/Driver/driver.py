import datetime

from flask import request

from .constants import *
from .errors import Driver_Not_Exist_Error, Json_InValid, InCorrect_Password_Error, Format_email_Invalid
from ...Common.Database import Database
from ...Common.Utilites import Utils


class Driver(object):

    def __init__(self):
        pass

    @staticmethod
    def check_details_valid(email, password):
        if not Utils.email_Isvalid(email):
            raise Format_email_Invalid('email format not valid')

        driver_data = Driver.find_driver(query={'email': email})
        if driver_data is None:
            raise Driver_Not_Exist_Error("your driver does not exist.")

        if not Utils.password_Isvalid(password, driver_data['Password']):
            raise InCorrect_Password_Error("wrong password associated with user email")

        return driver_data

    @staticmethod
    def check_json_vaild():  # checking the json file has two keys (email and password), if not, then  raise an error indicating the type of error.
        try:
            content = request.get_json()
            email = content['email']
            password = content['password']
            return email, password
        except KeyError:
            raise Json_InValid('The Json file is not valid')

    @staticmethod
    def find_driver(query):
        return Database.find_one(collection=DB_collection_Driver_collection, query=query)

    @staticmethod
    def login():
        email, password = Driver.check_json_vaild()
        driver_details = Driver.check_details_valid(email, password)
        Driver.current_driver_shift(driver_details)
        token = Utils.Create_Token(email)
        return token

    @staticmethod
    def current_driver_shift(query):  # storing the driver in database as current driver shift
        query.pop('Password')  # we don't need the password to save it in current shift
        d = datetime.datetime.now().strftime("%H:%M")  # adding the time when the driver start the shift
        query.update({"started from": d, Index_field_for_ttl: datetime.datetime.utcnow()})
        try:
            Database.save_to_db(collection=DB_collection_current_driver_shift, query=query)
        except:
            pass


    def save_to_db(self):
        pass

    def json(self):
        pass
