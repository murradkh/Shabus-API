import datetime
import re

import bcrypt
import jwt

from ..config import TOKEN_LIFETIME, SECRET_KEY


class Utils(object):

    @staticmethod
    def email_Isvalid(email):
        email_address_matcher = re.compile('^[\w\._%+-]+@([\w-]+\.)+[A-Za-z]{2,4}$')
        return email_address_matcher.match(email)

    @staticmethod
    def password_Isvalid(password, hashed_password):
        return bcrypt.checkpw(password.encode(), hashed_password.encode())

    @staticmethod
    def phone_number_Isvalid(phone_number):
        phone_number_matcher = re.compile('^05[\d]{8}$')
        return phone_number_matcher.match(phone_number)

    @staticmethod
    def id_number_Isvalid():
        return True

    @staticmethod
    def Create_Token(id):
        token = jwt.encode({'user': id, 'exp': (datetime.datetime.utcnow() + datetime.timedelta(hours=int(TOKEN_LIFETIME)))}, key=SECRET_KEY)
        return token.decode('utf-8')

    @staticmethod
    def Token_Isvalid(token):
        try:
            jwt.decode(token, SECRET_KEY)

            return True
        except:
            return False
