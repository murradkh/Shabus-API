class MoovitError(Exception):

    def __init__(self, message):
        self.message = message


class MoovitFeatureUsedBefore(MoovitError):
    pass


class JsonInValid(MoovitError):
    pass


class TokenIsInValid(MoovitError):
    pass


class FormatPhoneNumberInValid(MoovitError):
    pass
