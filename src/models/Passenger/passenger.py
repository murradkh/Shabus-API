from flask import request
class Passenger(object):

    def __init__(self):
        pass

    @staticmethod
    def check_Json_vaild():
        try:
            content = request.get_json()
            token = content.get('Token')
            # add here  phone number
        except:
            pass
            # raise  # add here the error
