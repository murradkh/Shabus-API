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
    def check_json_valid():
        try:
            content = request.get_json()
            return content['phone_number'], content['Token']
        except KeyError:
            raise JsonInValid('The Json file is not valid')

    @staticmethod
    def use_moovit_feature():

        phone_number, token = Moovit.check_json_valid()
        Utils.phone_number_Isvalid(phone_number=phone_number)
        query = {}
        decoded_token = Utils.decode_token(token=token)
        query['Wًith_Driver'] = decoded_token['name']
        query['Riding_Place'] = \
            Driver.get_coordination({'email': decoded_token['email']}, {'Current_location': 1, '_id': 0})[
                'Current_location']  # important thing i did here, its telling the mongo database to give me just the one field without other fields in document(which satisfy the requirements)
        query.update(phone_number=phone_number, _id=uuid.uuid4().hex,
                     Riding_Time=datetime.datetime.now().strftime("%Y/%m/%d, %H:%M"))
        Moovit.save_to_db(query=query)
        SMS.send_sms(phone_number=phone_number, text=INVITAION_MESSAGE)

    @staticmethod
    def save_to_db(query):
        try:
            Database.find_one(collection=DB_COLLECTION_USERS_USED_MOOVIT, query={"phone_number": query['phone_number']})
            raise MoovitFeatureUsedBefore("user used moovit feature before!")
        except CommonErrors:
            Database.save_to_db(collection=DB_COLLECTION_USERS_USED_MOOVIT, query=query)
