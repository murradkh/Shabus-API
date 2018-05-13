from flask import request, json
from ...Common.Database import Database
from .constants import COLLECTION
from ...Common.Utilites import Utils
from .errors import Driver_Not_Exist_Error, Json_InValid, InCorrect_Password_Error, Format_email_Invalid


class Driver(object):

    def __init__(self):
        pass

    @staticmethod
    def check_login_valid(email, password):

        if not Utils.email_Isvalid(email):
            raise Format_email_Invalid('email format not valid')

        driver_data = Database.find_one(collection=COLLECTION, query={'email': email})

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
