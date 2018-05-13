from flask import request

from .constants import COLLECTION
from .errors import Driver_Not_Exist_Error, Json_InValid, InCorrect_Password_Error, Format_email_Invalid
from ...Common.Database import Database
from ...Common.Utilites import Utils


class Driver(object):

    def __init__(self):
        pass

    @staticmethod
    def check_details_valid(email, password):  # checking

        if not Utils.email_Isvalid(email):
            raise Format_email_Invalid('email format not valid')

        driver_data = Driver.find_driver(query={'email': email})

        if driver_data is None:
            raise Driver_Not_Exist_Error("your driver does not exist.")

        if not Utils.password_Isvalid(password, driver_data['Password']):
            raise InCorrect_Password_Error("wrong password associated with user email")

        return driver_data

    @staticmethod
    def check_Json_vaild():  # checking the json file has two keys (email and password), if not, then  raise an error indicating the type of error.
        try:
            content = request.get_json()
            email = content['email']
            password = content['password']
            return email, password
        except:
            raise Json_InValid('The Json file is not valid')

    @staticmethod
    def find_driver(query):
        return Database.find_one(collection=COLLECTION, query=query)

    @staticmethod
    def login():

        email, password = Driver.check_Json_vaild()  # checking the json file have valid fields
        driver_details = Driver.check_details_valid(email,
                                                    password)  # checking the user data is valid with database data
        token = Utils.Create_Token(
            driver_details['_id'])  # Creating token according to user id(more safer than according the user email)
        return token

    def save_to_db(self):
        pass

    def json(self):
        pass
