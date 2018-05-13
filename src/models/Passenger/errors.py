class Passenger_Error(Exception):

    def __init__(self, message):
        self.message = message


class Json_InValid(Passenger_Error):
    pass


class Format_PhoneNumber_InValid(Passenger_Error):
    pass


class Format_ID_InValid(Passenger_Error):
    pass


class Passenger_NotExist_Error(Passenger_Error):
    pass


class Token_Is_InValid(Passenger_Error):
    pass
