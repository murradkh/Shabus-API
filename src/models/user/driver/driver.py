import datetime
import uuid

from flask import request

from src.common.database import Database
from src.common.utilites import Utils
from .constants import *
from .errors import *


class Driver(object):

    @staticmethod
    def check_details_valid(email,
                            password):  # checks if the details of the driver is valid against the Database, and returns the id of the driver if it is valid
        if not Utils.email_Isvalid(email):
            raise FormatEmailInvalid('email format not valid')

        driver_data = Driver.find_driver(query={'email': email})
        if driver_data is None:
            raise DriverNotExistError("your driver does not exist.")

        if not Utils.password_Isvalid(password, driver_data['Password']):
            raise InCorrectPasswordError("wrong password associated with user email")

        return driver_data['_id'], "" if driver_data.get('name') is None else driver_data['name']

    @staticmethod
    def check_json_vaild():  # checking the json file has two keys (email and password), if not, then  raise an error indicating the type of error.
        try:
            content = request.get_json()
            return content
        except KeyError:
            raise JsonInValid('The Json file is not valid')

    @staticmethod
    def find_driver(query):
        return Database.find_one(collection=DB_collection_Driver, query=query)

    @staticmethod
    def login():
        content = Driver.check_json_vaild()
        content['_id'], content['name'] = Driver.check_details_valid(content['email'], content['password'])
        Driver.store_driver_shift(content)
        token = Utils.Create_Token(content)

        return token

    @staticmethod
    def get_coordination(query, options):
        return Database.find_one(collection=DB_collection_current_driver_shift, query=query, options=options)

    @staticmethod
    def store_driver_shift(query):  # storing the driver in database as current driver shift
        query.pop('password')  # we don't need the password to save it in current shift
        d = datetime.datetime.now().strftime("%H:%M")  # adding the time when the driver start the shift
        query.update({"started from": d, "date": datetime.datetime.utcnow().strftime("%Y/%m/%d")})
        try:
            Database.save_to_db(collection=DB_collection_current_driver_shift, query=query)
        except Exception as e:  # thats in case the driver already exist in the driver shift collection.
            print(e.__doc__)

    @staticmethod
    def update_coordination():
        content = Driver.check_json_vaild()
        token = content['Token']
        coordination = content['coordination']
        decoded_token = Utils.decode_token(token=token)
        if decoded_token is None:
            raise TokenIsInValid('the token is not valid!')

        Database.update(DB_collection_current_driver_shift, {'email': decoded_token['email']},
                        {"coordination": coordination}, False)

    @staticmethod
    def logout():
        content = Driver.check_json_vaild()
        token = content.get('Token')
        decoded_token = Utils.decode_token(token=token)
        if decoded_token is None:
            raise TokenIsInValid('the token is not valid!')
        current_shift = Database.find_one_and_delete(collection=DB_collection_current_driver_shift,
                                                     query={'email': decoded_token['email']})
        current_shift['finished at'] = datetime.datetime.now().strftime('%H:%M')
        current_shift[
            '_id'] = uuid.uuid4().hex  # here i changed the id of the document for not happening contradiction of the documents (which same driver can exist many times in this collection)
        Database.save_to_db(collection=DB_collection_previous_driver_shift, query=current_shift)
