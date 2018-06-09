class CommonErrors(Exception):
    def __init__(self, message):
        self.message = message


class TokenInValid(CommonErrors):
    pass


class FormatPhoneNumberInValid(CommonErrors):
    pass


class SmsError(CommonErrors):
    pass


class DBErrors(CommonErrors):
    pass


class FormatEmailInvalid(CommonErrors):
    pass


class PasswordInValid(CommonErrors):
    pass


class HashingPasswordFailed(CommonErrors):
    pass

