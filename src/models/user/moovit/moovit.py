import datetime
import uuid

from flask import request
from twilio.base.exceptions import TwilioRestException, TwilioException

from src.common.database import Database
from src.common.sms import SMS
from src.common.utilites import Utils
from src.models.user.driver.driver import Driver
from .constants import *
from .errors import *


class Moovit(object):
    INVITAION_MESSAGE = "תודה לך שבחרת בשבוס.\nאם רוצים להיות חברים בשבוס תלחצו על הלינק:\n https://app.shabus.co.il/register/"

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
        if not Utils.phone_number_Isvalid(phone_number=phone_number):
            raise FormatPhoneNumberInValid("the format of phone number is invalid!")
        if not Utils.Token_Isvalid(token=token):
            raise TokenIsInValid("the token is invalid!")

        query = {}
        decoded_token = Utils.decode_token(token=token)
        query['with driver'] = decoded_token['email']
        query['the riding place'] = \
            Driver.get_coordination({'email': decoded_token['email']}, {'coordination': 1, '_id': 0})[
                'coordination']  # important thing i did here, its telling the mongo database to give me just the one field without other fields in document(which satisfy the requirements)
        query.update(phone_number=phone_number, _id=uuid.uuid4().hex,
                     riding_time=datetime.datetime.now().strftime("%Y/%m/%d, %H:%M"))
        Moovit.save_to_db(query=query)
        print(phone_number, Moovit.INVITAION_MESSAGE)
        try:
            SMS.send_sms(phone_number=phone_number, text=Moovit.INVITAION_MESSAGE)
        except (TwilioRestException, TwilioException) as e:
            print(e)
            raise SmsError("sending the message to phone number is failed, maybe because the phone number i invalid")

    @staticmethod
    def save_to_db(query):
        if Database.find_one(collection=DB_COLLECTION_USERS_USED_MOOVIT,
                             query={"phone_number": query['phone_number']}) is None:
            Database.save_to_db(collection=DB_COLLECTION_USERS_USED_MOOVIT, query=query)
        else:
            raise MoovitFeatureUsedBefore("user used moovit feature before!")
