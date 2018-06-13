import datetime
import random
import uuid

from flask import request

from src.common.database import Database
from src.common.errors import DBErrors
from src.common.sms import SMS
from src.common.utilites import Utils
from .constants import *
from .errors import *


class Driver(object):

    @staticmethod
    def check_email_validation(email):
        Utils.email_Isvalid(email)
        driver_data = Driver.find_driver(query={'Email': email})
        return driver_data

    @staticmethod
    def check_password_validation(password, driver_data):
        Utils.password_isvalid(password, PASSWORD_MIN_LENGTH, PASSWORD_PATTERN)
        if not Utils.passwords_matching(password, driver_data['Password']):
            raise InCorrectPasswordError("wrong password associated with user phoneNumber")

    @staticmethod
    def check_phone_number_validation(phone_number):
        Utils.phone_number_Isvalid(phone_number=phone_number)
        driver_data = Driver.find_driver(query={'PhoneNumber': phone_number})
        return driver_data

    @staticmethod
    def forget_password():
        phone_number, = Utils.check_json_vaild(request.get_json(), 'PhoneNumber')
        driver_data = Driver.check_phone_number_validation(phone_number=phone_number)
        code_number = random.randrange((10 ** (FORGET_PASSWORD_CODE_LENGTH - 1) + 1), 10 ** FORGET_PASSWORD_CODE_LENGTH,
                                       1)
        SMS.send_sms(driver_data['PhoneNumber'],
                     FORGET_PASSWORD_SMS_MESSAGE + str(code_number))
        restoration_code = dict()
        restoration_code['Password restoration code'] = code_number
        Driver.update_db({"PhoneNumber": phone_number}, restoration_code)
        token = Utils.create_token({"PhoneNumber": driver_data['PhoneNumber']}, life_time_minutes=CODE_NUMBER_DURATION)
        image = Driver.get_image({"PhoneNumber": driver_data['PhoneNumber']})
        return token, image

    @staticmethod
    def change_password():
        token, new_password = Utils.check_json_vaild(request.get_json(), 'Token', 'NewPassword')
        Utils.password_isvalid(new_password, PASSWORD_MIN_LENGTH, PASSWORD_PATTERN)
        decoded_token = Utils.decode_token(token)
        hashed_password = Utils.hash_password(new_password)
        Driver.update_db({'PhoneNumber': decoded_token['PhoneNumber']},
                         {"Password": hashed_password})

    @staticmethod
    def check_code_number_validation():
        restoration_code, token = Utils.check_json_vaild(request.get_json(), 'Restoration code', "Token")
        decoded_token = Utils.decode_token(token)
        driver_data = Driver.find_driver(query={'PhoneNumber': decoded_token['PhoneNumber']},
                                         options={'Password restoration code': 1})
        if driver_data['Password restoration code'] != int(restoration_code):
            raise CodeNumberIsInValid("the code number is invalid!")

        token_data = {"PhoneNumber": decoded_token['PhoneNumber']}
        return Utils.create_token(token_data, life_time_minutes=CHANGING_PASSWORD_DURATION)

    @staticmethod
    def registration():
        name, phone_number, email, password, birthday, image = Utils.check_json_vaild(request.get_json(), 'Name',
                                                                                      "PhoneNumber", 'Email',
                                                                                      'Password', 'Birthday', 'Image')
        try:
            Driver.check_phone_number_validation(phone_number=phone_number)
        except DriverError:
            try:
                Driver.check_email_validation(email=email)
            except DriverNotExistError:
                Utils.password_isvalid(password, PASSWORD_MIN_LENGTH, PASSWORD_PATTERN)
                hashed_password = Utils.hash_password(password)
                query = {"Name": name, "PhoneNumber": phone_number, "Email": email, 'Birthday': birthday,
                         "Password": hashed_password,
                         "_id": uuid.uuid4().hex,
                         "Confirmed account": False}
                Database.save_to_db(collection=DB_COLLECTION_DRIVER, query=query)
                Driver.save_image({"Name": name, "PhoneNumber": phone_number}, image)
                SMS.send_sms(phone_number,
                             ACTIVATING_ACCOUNT_SMS_MESSAGE + "\nhttps://shabus-21aa4.firebaseapp.com/confirmation/" + str(
                                 query['_id']))
            else:
                raise DriverExistError("the driver email already exist!")
        else:
            raise DriverExistError("the driver phone number already exist!")

    @staticmethod
    def edit_details():
        token, = Utils.check_json_vaild(request.get_json(), "Token")
        decoded_token = Utils.decode_token(token=token)
        Driver.delete_driver(decoded_token['PhoneNumber'])
        Driver.registration()
        name, phone_number, email, birthday = Utils.check_json_vaild(request.get_json(), 'Name', "PhoneNumber", "Email",
                                                                     'Birthday')
        new_token = Utils.create_token(
            {"Name": name, "PhoneNumber": phone_number, "Email": email, "Birthday": birthday},
            life_time_hours=TOKEN_LIFETIME)
        return new_token

    @staticmethod
    def find_driver(query, options=None):
        try:
            return Database.find_one(collection=DB_COLLECTION_DRIVER, query=query, options=options)
        except DBErrors:
            raise DriverNotExistError("driver does not exist.")

    @staticmethod
    def login():
        phone_number, password, coordination = Utils.check_json_vaild(request.get_json(), 'PhoneNumber', "Password",
                                                                      'Coordination')
        driver_data = Driver.check_phone_number_validation(phone_number=phone_number)
        Driver.check_password_validation(password, driver_data)
        if driver_data['Confirmed account'] is False:
            raise AccountNotActivated("the account not yet activated!")
        Driver.store_driver_shift(driver_data, coordination)
        wanted_keys = {'Name', 'PhoneNumber', 'Email', 'Birthday'}
        token_data = {key: value for key, value in driver_data.items() if key in wanted_keys}
        token = Utils.create_token(token_data, life_time_hours=TOKEN_LIFETIME)
        image = Driver.get_image({"PhoneNumber": phone_number})
        return token, image

    @staticmethod
    def get_coordination(query, options):
        return Database.find_one(collection=DB_collection_current_driver_shift, query=query, options=options)

    @staticmethod
    def store_driver_shift(query, coordination):  # storing the driver in database as current driver shift
        query.pop('Password')
        query.pop('Birthday')
        query.pop('Confirmed account')

        d = datetime.datetime.now().strftime("%H:%M")  # adding the time when the driver start the shift
        query.update(
            {"Started at": d, 'Start location': coordination, "Date": datetime.datetime.utcnow().strftime("%Y/%m/%d"),
             'created_at': datetime.datetime.utcnow(), 'Current location': coordination})
        try:
            Database.save_to_db(collection=DB_collection_current_driver_shift, query=query)
        finally:
            pass

    @staticmethod
    def update_coordination():
        token, coordination = Utils.check_json_vaild(request.get_json(), "Token", "Coordination")
        decoded_token = Utils.decode_token(token=token)
        Database.update(DB_collection_current_driver_shift, {'Email': decoded_token['Email']},
                        {"Current location": coordination}, False)

    @staticmethod
    def logout():
        token, = Utils.check_json_vaild(request.get_json(), "Token")
        decoded_token = Utils.decode_token(token=token)
        current_shift = Database.find_one_and_delete(collection=DB_collection_current_driver_shift,
                                                     query={'Email': decoded_token['Email']})
        current_shift['Finished at'] = datetime.datetime.now().strftime('%H:%M')
        current_shift[
            '_id'] = uuid.uuid4().hex  # here i changed the id of the document for not happening contradiction of the documents (which same driver can exist many times in this collection)
        current_shift['End location'] = current_shift['Current location']
        current_shift.pop('Current location')
        Database.save_to_db(collection=DB_collection_previous_driver_shift, query=current_shift)

    @staticmethod
    def update_db(query, update, upsert=False):
        Database.update(DB_COLLECTION_DRIVER, query, update, upsert)

    @staticmethod
    def get_image(filter):
        return Database.find_image(collection=DB_COLLECION_IMAGES, filter=filter)

    @staticmethod
    def save_image(image_details, image):
        Database.save_image(collection=DB_COLLECION_IMAGES, image_details=image_details, image=image)

    @staticmethod
    def delete_driver(phone_number):
        Database.delete(DB_COLLECTION_DRIVER, {"PhoneNumber": phone_number})
        Database.delete_image(DB_COLLECION_IMAGES, {"PhoneNumber": phone_number})

    @staticmethod
    def confirmation_of_driver_account():
        id, = Utils.check_json_vaild(request.get_json(), "id")
        data = Driver.find_driver({"_id": id}, {"Name": 1})
        Driver.update_db({'_id': id}, {"Confirmed account": True})
        return data['Name']
