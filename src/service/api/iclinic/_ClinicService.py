from typing import Dict

from src.utils import Request


class ClinicService:
    def __init__(self, url, auth_token):
        self.url = url
        self.auth_token = auth_token
        self.request = Request(2, auth_token=self.auth_token, cache_minutes=4320, timeout=5, retries=3)

    def get(self, clinic_id):
        # type: (int) -> Dict
        return self.request.get(self.url + str(clinic_id) + '/')
