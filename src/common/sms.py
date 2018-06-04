from twilio.base.exceptions import TwilioRestException, TwilioException
from twilio.rest import Client

from src.config import TWILIO_AUTH_TOKEN, TWILIO_ACCOUNT_SID, PHONE_NUMBER
from .errors import SmsError


class SMS(object):
    CLIENT = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    @staticmethod
    def send_sms(phone_number, text):
        try:
            return SMS.CLIENT.messages.create(
                to="+972" + phone_number,
                from_=PHONE_NUMBER,
                body=text)
        except (TwilioRestException, TwilioException):
            raise SmsError("sending the message to phone number is failed, maybe because the phone number i invalid")

# def is_phone_number(number):
#     print isinstance(number, (str, unicode))
#     print number.startswith("05")
#     print len(number) == 10
#     return isinstance(number, (str, unicode)) and number.startswith("05") and len(number) == 10
