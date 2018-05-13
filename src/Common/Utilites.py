import datetime
import re

import bcrypt
import jwt

from ..config import TOKEN_LIFETIME, SECRET_KEY


class Utils(object):

    # @staticmethod
    # def check_hashed_password(password, hashed_password):
    #     return False
    #
    # @staticmethod
    # def hash_password(password):
    #     return True

    @staticmethod
    def email_Isvalid(email):
        email_address_matched = re.compile('^[\w-]+@([\w-]+\.)+[\w]+$')
        return email_address_matched.match(email)

    @staticmethod
    def password_Isvalid(password, hashed_password):
        return bcrypt.checkpw(password.encode(), hashed_password.encode())

    @staticmethod
    def phone_number_Isvalid(phone_number):
        return True

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
