class DriverError(Exception):
    def __init__(self, message):
        self.message = message


class DriverNotExistError(DriverError):
    pass


class DriverExistError(DriverError):
    pass


class InCorrectPasswordError(DriverError):
    pass


class CodeNumberIsInValid(DriverError):
    pass


class AccountNotActivated(DriverError):
    pass
