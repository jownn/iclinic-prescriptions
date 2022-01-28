from typing import Dict

from src.utils import Request


class PatientService:
    def __init__(self, url, auth_token):
        self.url = url
        self.auth_token = auth_token
        self.request = Request(4, auth_token=self.auth_token, cache_minutes=720, timeout=3, retries=2)

    def get(self, patient_id):
        # type: (int) -> Dict
        return self.request.get(self.url + str(patient_id) + '/')
