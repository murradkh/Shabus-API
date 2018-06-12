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
        image = Manager.get_image({"PhoneNumber": phone_number})
        return token, image

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
    def get_image(filter):
        return Database.find_image(collection=DB_COLLECION_IMAGES, filter=filter)
