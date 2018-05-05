class Driver_Error(Exception):
    def __init__(self, message):
        self.message = message


class Driver_Not_Exist_Error(Driver_Error):
    pass

class InCorrect_Password_Error(Driver_Error):
    pass


class Form_InValid(Driver_Error):
    pass

class Format_email_Invalid(Driver_Error):
    pass
