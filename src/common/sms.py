from twilio.rest import Client

from src.config import TWILIO_AUTH_TOKEN, TWILIO_ACCOUNT_SID


class SMS(object):
    CLIENT = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    PHONE_NUMBER = u"Shabus"

    # ACTIVATION_CODE_TEXT = "Welcome to shabus. Your code is %0" + str(models.CODE_LENGTH) + "d."

    @staticmethod
    def send_sms(phone_number, text):
        return SMS.CLIENT.messages.create(
            to="+972" + phone_number,
            from_=SMS.PHONE_NUMBER,
            body=text)


# def send_activation_code(phone_number, code):
#     m = client.messages.create(
#             to=phone_number,
#             from_=PHONE_NUMBER,
#             body=ACTIVATION_CODE_TEXT%code,
#     )
#     return m
#
# def delete_log(message_sid):
#     return client.messages.delete(message_sid)
#
#
# def is_phone_number(number):
#     print isinstance(number, (str, unicode))
#     print number.startswith("05")
#     print len(number) == 10
#     return isinstance(number, (str, unicode)) and number.startswith("05") and len(number) == 10
