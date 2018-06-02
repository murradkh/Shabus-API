class DriverError(Exception):
    def __init__(self, message):
        self.message = message


class DriverNotExistError(DriverError):
    pass


class InCorrectPasswordError(DriverError):
    pass


class JsonInValid(DriverError):
    pass


class FormatEmailInvalid(DriverError):
    pass


class TokenIsInValid(DriverError):
    pass
