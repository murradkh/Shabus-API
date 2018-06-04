class CommonErrors(Exception):
    def __init__(self, message):
        self.message = message


class TokenIsInValid(CommonErrors):
    pass


class FormatPhoneNumberInValid(CommonErrors):
    pass


class SmsError(CommonErrors):
    pass


class DBErrors(CommonErrors):
    pass
