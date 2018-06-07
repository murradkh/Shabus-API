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
        if not email_address_matcher.match(email):
            raise FormatEmailInvalid('email format not valid')

    @staticmethod
    def password_isvalid(password, min_length):
        matcher = re.compile("^(([0-9]+[a-zA-z]+[0-9]*)|([a-zA-Z]+[0-9]+[a-zA-Z]*))+$")
        if not (matcher.match(password) and len(password) >= min_length):
            raise PasswordInValid("the password not according to the rules")

    @staticmethod
    def passwords_matching(password, hashed_password):
        return bcrypt.checkpw(password.encode(), hashed_password.encode())

    @staticmethod
    def hash_password(password):
        try:
            return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        except:
            raise HashingPasswordFailed(
                "the hashing function failed to encrypt the password, maybe because the password is invalid")

    @staticmethod
    def phone_number_Isvalid(phone_number):
        phone_number_matcher = re.compile('^05[\d]{8}$')
        if not (isinstance(phone_number, str) and phone_number_matcher.match(phone_number)):
            raise FormatPhoneNumberInValid('phone number invalid!')

    @staticmethod
    def create_token(content, life_time_minutes=0, life_time_hours=0):
        d = dict(content)
        d.update(exp=(datetime.datetime.utcnow() + datetime.timedelta(hours=int(life_time_hours),
                                                                      minutes=int(life_time_minutes))))
        token = jwt.encode(d, key=SECRET_KEY)
        return token.decode('utf-8')

    @staticmethod
    def decode_token(token):
        try:
            return jwt.decode(token, SECRET_KEY)
        except:
            raise TokenInValid('the token is not valid!')
