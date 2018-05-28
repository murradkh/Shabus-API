import datetime
import re

import bcrypt
import jwt

from ..config import TOKEN_LIFETIME, SECRET_KEY


class Utils(object):

    @staticmethod
    def email_Isvalid(email):
        email_address_matcher = re.compile('^[\w_%+-.]+@([\w-]+\.)+[A-Za-z]{2,4}$')
        return email_address_matcher.match(email)

    @staticmethod
    def password_Isvalid(password, hashed_password):
        return bcrypt.checkpw(password.encode(), hashed_password.encode())

    @staticmethod
    def phone_number_Isvalid(phone_number):
        # return isinstance(number, (str, unicode)) and number.startswith("05") and len(number) == 10 # this is alternative way to check the phone number is valid
        phone_number_matcher = re.compile('^05[\d]{8}$')
        return isinstance(phone_number, str) and phone_number_matcher.match(phone_number)

    @staticmethod
    def id_number_Isvalid():
        return True

    @staticmethod
    def Create_Token(email):
        token = jwt.encode(
            {'user': email, 'exp': (datetime.datetime.utcnow() + datetime.timedelta(hours=int(TOKEN_LIFETIME)))},
            key=SECRET_KEY)
        return token.decode('utf-8')

    @staticmethod
    def Token_Isvalid(token):

        if Utils.decode_token(token=token) is None:
            return False
        return True

    @staticmethod
    def decode_token(token):
        try:
            return jwt.decode(token, SECRET_KEY)
        except:
            return None
