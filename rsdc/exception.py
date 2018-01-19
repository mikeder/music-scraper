

class BaseException(Exception):
    def __init__(self, status_code, platform_code, error_string, response=None):
        self.status_code = status_code
        self.platform_code = platform_code
        self.message = error_string
        self.response = response
        self.status_reason = ''


class ConfigLoadError(BaseException):
    def __init__(self, status_code, platform_code, error_string):
        super(ConfigLoadError, self).__init__(status_code, platform_code, error_string)


class DataException(BaseException):
    def __init__(self, status_code, platform_code, error_string):
        super(DataException, self).__init__(status_code, platform_code, error_string)


class HTTPException(BaseException):
    def __init__(self, status_code, platform_code, error_string):
        super(HTTPException, self).__init__(status_code, platform_code, error_string)


class UnknownHttpException(BaseException):
    def __init__(self, status_code, platform_code, error_string):
        super(UnknownHttpException, self).__init__(status_code, platform_code, error_string)