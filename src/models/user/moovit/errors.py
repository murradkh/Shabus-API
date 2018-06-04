class MoovitError(Exception):

    def __init__(self, message):
        self.message = message


class MoovitFeatureUsedBefore(MoovitError):
    pass


class JsonInValid(MoovitError):
    pass


