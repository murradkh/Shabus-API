from flask import request

from ...Common.Database import Database
from .constants import COLLECTION
from ...Common.Utilites import Utils
from .errors import Driver_Not_Exist_Error, Form_InValid, InCorrect_Password_Error, Format_email_Invalid


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

        return True

    @staticmethod
    def check_Form_vaild():  # checking the form has two arguments (email and password), if not, then  raise an error indicating the type of error.
        try:
            email = request.form['email']
            password = request.form['password']
            return email, password
        except:
            raise Form_InValid('The form is not valid')
