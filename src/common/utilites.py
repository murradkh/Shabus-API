import datetime
import re

import bcrypt
import jwt

from src.common.errors import *
from ..config import SECRET_KEY


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
        if not (isinstance(phone_number, str) and phone_number_matcher.match(phone_number)):
            raise FormatPhoneNumberInValid('phone number invalid!')

    @staticmethod
    def Create_Token(content, life_time_minutes=0, life_time_hours=0):
        d = dict(content)
        d.update(exp=(datetime.datetime.utcnow() + datetime.timedelta(hours=int(life_time_hours),
                                                                      minutes=int(life_time_minutes))))
        print(d)
        token = jwt.encode(d, key=SECRET_KEY)
        return token.decode('utf-8')

    @staticmethod
    def decode_token(token):
        try:
            return jwt.decode(token, SECRET_KEY)
        except:
            raise TokenIsInValid('the token is not valid!')
