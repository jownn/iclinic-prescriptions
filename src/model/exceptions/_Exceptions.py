class RequestException(Exception):
    def __init__(self, status_code: int, message: str, code: int):
        self.status_code = status_code
        self.message = message
        self.code = code
