import bcrypt
import re


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
    def phone_number_Isvalid():
        return True

    @staticmethod
    def id_number_Isvalid():
        return True
