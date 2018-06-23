import datetime
import uuid

from flask import request

from src.common.database import Database
from src.common.sms import SMS
from src.common.utilites import Utils, CommonErrors
from src.models.user.driver.driver import Driver
from .constants import *
from .errors import *


class Moovit(object):

    @staticmethod
    def use_moovit_feature():
        phone_number, token = Utils.check_json_vaild(request.get_json(), "PhoneNumber", "Token")
        Utils.phone_number_Isvalid(phone_number=phone_number)
        query = {}
        decoded_token = Utils.decode_token(token=token)
        query['Wًith driver'] = decoded_token['Name']
        query['Riding place'] = \
            Driver.get_coordination({'Email': decoded_token['Email']}, {'Current location': 1, '_id': 0})[
                'Current location']  # important thing i did here, its telling the mongo database to give me just the one field without other fields in document(which satisfy the requirements)
        query.update({"PhoneNumber": phone_number, "_id": uuid.uuid4().hex,
                      "Riding time": (datetime.datetime.now() + datetime.timedelta(hours=3)).strftime(
                          "%Y/%m/%d, %H:%M")})
        Moovit.save_to_db(query=query)
        SMS.send_sms(phone_number=phone_number, text=INVITAION_MESSAGE)

    @staticmethod
    def save_to_db(query):
        try:
            Database.find_one(collection=DB_COLLECTION_USERS_USED_MOOVIT, query={"PhoneNumber": query['PhoneNumber']})
            raise MoovitFeatureUsedBefore("user used moovit feature before!")
        except CommonErrors:
            Database.save_to_db(collection=DB_COLLECTION_USERS_USED_MOOVIT, query=query)
