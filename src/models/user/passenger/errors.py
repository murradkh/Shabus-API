class PassengerError(Exception):

    def __init__(self, message):
        self.message = message


class JsonInValid(PassengerError):
    pass


class FormatIDInValid(PassengerError):
    pass


class ViolationNumberOfPassengers(PassengerError):
    pass


class PassengerNotExistError(PassengerError):
    pass


class TokenIsInValid(PassengerError):
    pass
