import datetime
import random
import uuid

from flask import request

from src.common.database import Database
from src.common.sms import SMS
from src.common.utilites import Utils
from .constants import *
from .errors import *


class Driver(object):

    @staticmethod
    def check_email_validation(email):
        if not Utils.email_Isvalid(email):
            raise FormatEmailInvalid('email format not valid')

        driver_data = Driver.find_driver(query={'email': email})
        if driver_data is None:
            raise DriverNotExistError("your driver does not exist.")
        return driver_data

    @staticmethod
    def check_password_validation(password, driver_data):
        if not Utils.password_Isvalid(password, driver_data['Password']):
            raise InCorrectPasswordError("wrong password associated with user email")

    @staticmethod
    def check_phone_number_validation(phone_number):

        Utils.phone_number_Isvalid(phone_number=phone_number)
        driver_data = Driver.find_driver(query={'phone_number': phone_number})
        return driver_data

    @staticmethod
    def forget_password():
        phone_number, = Driver.check_json_vaild('phone_number')
        driver_data = Driver.check_phone_number_validation(phone_number=phone_number)
        code_number = random.randrange((10 ** (FORGET_PASSWORD_CODE_LENGTH - 1) + 1), 10 ** FORGET_PASSWORD_CODE_LENGTH,
                                       1)
        SMS.send_sms(driver_data['phone_number'],
                     FORGET_PASSWORD_SMS_MESSAGE + str(code_number))
        restoration_code = dict()
        restoration_code['restoration_code'] = code_number
        restoration_code['created_at'] = datetime.datetime.now()
        Driver.update_db({"phone_number": phone_number}, {"password_restoration": restoration_code})

    @staticmethod
    def change_password():
        pass

    @staticmethod
    def check_code_number_validation():
        restoration_code, phone_number = Driver.check_json_vaild('restoration_code', "phone_number")
        driver_data = Driver.check_phone_number_validation(phone_number=phone_number)
        if (driver_data.get("password_restoration") is None) or (
                driver_data["password_restoration"]['restoration_code'] != restoration_code) or (
                (datetime.datetime.now() - datetime.timedelta(minutes=CODE_NUMBER_DURATION)) >
                driver_data["password_restoration"]['created_at']):
            raise CodeNumberIsInValid("the code number is invalid!")

    @staticmethod
    def check_json_vaild(
            *args):
        try:
            content = request.get_json()
            return tuple([content[i] for i in args] if len(args) != 0 else content)
        except KeyError:
            raise JsonInValid('The Json file is not valid')

    @staticmethod
    def find_driver(query):
        data = Database.find_one(collection=DB_collection_Driver, query=query)
        if data is None:
            raise DriverNotExistError("driver does not exist.")
        return data

    @staticmethod
    def login():
        phone_number, password, coordination = Driver.check_json_vaild('phone_number', "password", 'coordination')
        driver_data = Driver.check_phone_number_validation(phone_number=phone_number)
        Driver.check_password_validation(password, driver_data)
        Driver.store_driver_shift(driver_data, coordination)
        token = Utils.Create_Token(driver_data)
        return token

    @staticmethod
    def get_coordination(query, options):
        return Database.find_one(collection=DB_collection_current_driver_shift, query=query, options=options)

    @staticmethod
    def store_driver_shift(query, coordination):  # storing the driver in database as current driver shift
        query.pop('Password')
        d = datetime.datetime.now().strftime("%H:%M")  # adding the time when the driver start the shift
        query.update(
            {"Started_at": d, 'Start_location': coordination, "Date": datetime.datetime.utcnow().strftime("%Y/%m/%d"),
             'created_at': datetime.datetime.utcnow(), 'Current_location': coordination})
        try:
            Database.save_to_db(collection=DB_collection_current_driver_shift, query=query)
        except:
            pass

    @staticmethod
    def update_coordination():
        token, coordination = Driver.check_json_vaild("Token", "coordination")
        decoded_token = Utils.decode_token(token=token)
        Database.update(DB_collection_current_driver_shift, {'email': decoded_token['email']},
                        {"Current_location": coordination}, False)

    @staticmethod
    def logout():
        token, = Driver.check_json_vaild("Token")
        decoded_token = Utils.decode_token(token=token)
        current_shift = Database.find_one_and_delete(collection=DB_collection_current_driver_shift,
                                                     query={'email': decoded_token['email']})
        current_shift['finished at'] = datetime.datetime.now().strftime('%H:%M')
        current_shift[
            '_id'] = uuid.uuid4().hex  # here i changed the id of the document for not happening contradiction of the documents (which same driver can exist many times in this collection)
        current_shift['End_location'] = current_shift['Current_location']
        current_shift.pop('Current_location')
        Database.save_to_db(collection=DB_collection_previous_driver_shift, query=current_shift)

    @staticmethod
    def update_db(query, update):
        Database.update(DB_collection_Driver, query, update)
