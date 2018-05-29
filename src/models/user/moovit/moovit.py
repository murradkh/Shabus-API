import datetime
import uuid

from flask import request

from src.common.database import Database
from src.common.utilites import Utils
from .constants import *
from .errors import *


class Moovit(object):

    @staticmethod
    def check_json_valid():
        try:
            content = request.get_json()
            return content['phone number'], content['Token']
        except KeyError:
            raise JsonInValid('The Json file is not valid')

    @staticmethod
    def use_moovit_feature():
        phone_number, token = Moovit.check_json_valid()
        if not Utils.phone_number_Isvalid(phone_number=phone_number):
            raise FormatPhoneNumberInValid("the format of phone number is invalid!")
        query = {}
        query.update(phone_number=phone_number, _id=uuid.uuid4().hex,
                     riding_time=datetime.datetime.now().strftime("%Y/%m/%d, %H:%M"))
        Moovit.save_to_db(query=query)

    @staticmethod
    def save_to_db(query):
        if Database.find_one(collection=DB_COLLECTION_USERS_USED_MOOVIT,
                             query={"phone_number": query['phone_number']}) is None:
            Database.save_to_db(collection=DB_COLLECTION_USERS_USED_MOOVIT, query=query)
        else:
            raise MoovitFeatureUsedBefore("user used moovit feature before!")
