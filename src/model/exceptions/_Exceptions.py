from enum import Enum


class ServicesError(Enum):
    DEFAULT = 1
    CLINIC = 2
    PHYSICIAN = 3
    PATIENT = 4
    METRICS = 5


class RequestException(Exception):
    def __init__(self, status_code: int, message: str, code: int):
        self.status_code = status_code
        self.message = message
        self.code = code


def get_exception(service: int, status_code: int, raise_error: bool = False) -> RequestException:
    message = ""
    code = 0
    if ServicesError.DEFAULT.value == service:
        if status_code == 422:
            message = "malformed request"
            code = 1
    if ServicesError.PHYSICIAN.value == service:
        if status_code == 404:
            message = "physician not found"
            code = 2
        if status_code == 503:
            message = "physicians service not available"
            code = 5
    if ServicesError.PATIENT.value == service:
        if status_code == 404:
            message = "patient not found"
            code = 3
        if status_code == 503:
            message = "patients service not available"
            code = 6
    if ServicesError.METRICS.value == service:
        if status_code == 503:
            message = "metrics service not available"
            code = 4

    exception = RequestException(status_code=status_code, message=message, code=code)
    if raise_error and message:
        raise exception
    return exception
