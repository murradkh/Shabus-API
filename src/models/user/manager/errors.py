class ManagerError(Exception):

    def __init__(self, message):
        self.message = message


class ManagerNotExistError(ManagerError):
    pass


class InCorrectPasswordError(ManagerError):
    pass


class JsonInValid(ManagerError):
    pass


class CodeNumberIsInValid(ManagerError):
    pass
