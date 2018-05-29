# import os
# from twilio.rest import Client
# import logging
# import random
# from ..config import ACCOUNT_SID,AUTH_TOKEN
#
# s = TwilioIpMessagingClient(ACCOUNT_SID, AUTH_TOKEN)
# PHONE_NUMBER = u"Shabus"
# ACTIVATION_CODE_TEXT = "Welcome to shabus. Your code is %0" + "murrad" + "d."
# srandom = random.SystemRandom()
#
# client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)
#
# logger = logging.getLogger("shabus.sms")
#
#
# def send_invitation(phone_number, text, callback_url):
#     try:
#         if callback_url is not None:
#             return client.messages.create(
#                 to=phone_number,
#                 from_=PHONE_NUMBER,
#                 body=text,
#                 status_callback=callback_url)
#         return client.messages.create(
#             to=phone_number,
#             from_=PHONE_NUMBER,
#             body=text)
#     except Exception as e:
#         logger.warn("Failed sending sms")
#         logger.exception(e)
#     return None
#
#
# def send_activation_code(phone_number, code):
#     m = client.messages.create(
#         to=phone_number,
#         from_=PHONE_NUMBER,
#         body=ACTIVATION_CODE_TEXT % code,
#     )
#     return m
#
#
# def delete_log(message_sid):
#     return client.messages.delete(message_sid)
#
# #
# # def is_phone_number(number):
# #
# #     print
# #     isinstance(number, str)
# #     print
# #     number.startswith("05")
# #     print
# #     len(number) == 10
# #     return isinstance(number, str) and number.startswith("05") and len(number) == 10
