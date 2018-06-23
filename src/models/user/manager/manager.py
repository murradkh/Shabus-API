from flask import request

from src.common.database import Database
from src.common.errors import DBErrors
from src.common.utilites import Utils
from src.models.user.manager.constants import *
from .errors import *


class Manager(object):

    @staticmethod
    def login():
        phone_number, password = Utils.check_json_vaild(request.get_json(), "PhoneNumber", "Password")
        manager_data = Manager.check_phone_number_validation(phone_number=phone_number)
        Manager.check_password_validation(password, manager_data)
        wanted_keys = {'Name', 'PhoneNumber'}
        token_data = {key: value for key, value in manager_data.items() if key in wanted_keys}
        token = Utils.create_token(token_data, life_time_hours=TOKEN_LIFETIME)
        # image = Manager.get_image({"PhoneNumber": phone_number})
        return token

    @staticmethod
    def check_phone_number_validation(phone_number):
        Utils.phone_number_Isvalid(phone_number=phone_number)
        manager_data = Manager.find_manager(query={'PhoneNumber': phone_number})
        return manager_data

    @staticmethod
    def find_manager(query, options=None):
        try:
            return Database.find_one(collection=DB_COLLECTION_MANAGER, query=query, options=options)
        except DBErrors:
            raise ManagerNotExistError("manager does not exist.")

    @staticmethod
    def check_password_validation(password, manager_data):
        Utils.password_isvalid(password, PASSWORD_MIN_LENGTH, PASSWORD_PATTERN)
        if not Utils.passwords_matching(password, manager_data['Password']):
            raise InCorrectPasswordError("wrong password associated with user phoneNumber")

    @staticmethod
    def get_data(collection):
        # images = Manager.gez
        token, = Utils.check_json_vaild(request.get_json(), "Token")
        Utils.decode_token(token=token)
        data = Database.find(collection=collection, query={},
                             options={'_id': 0, 'created_at': 0, 'Password restoration code': 0, 'Password': 0})
        data = [sorted(i.items(), key=lambda k: PRIORITIES[list(k)[0]]) for i in data]
        return data

    # @staticmethod
    # def get_image(filter):
    #     return Database.find_image(collection=DB_COLLECION_IMAGES, filter=filter)

    @staticmethod
    def delete(collection):
        token, phone_number = Utils.check_json_vaild(request.get_json(), "Token", 'PhoneNumber')
        Utils.decode_token(token=token)
        if collection == 'Passengers' or 'New rides':
            Database.delete(collection, {"phone_number": phone_number})
        elif collection == 'Drivers':
            Database.delete(collection, {"PhoneNumber": phone_number})
            Database.delete_image(DB_COLLECION_IMAGES, {"PhoneNumber": phone_number})
        else:
            Database.delete(collection, {"PhoneNumber": phone_number})
