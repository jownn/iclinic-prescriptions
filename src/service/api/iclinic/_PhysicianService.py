from typing import Dict

from src.utils import Request


class PhysicianService:
    def __init__(self, url, auth_token):
        self.url = url
        self.auth_token = auth_token
        self.request = Request(3, auth_token=self.auth_token, cache_minutes=2880, timeout=4, retries=2)

    def get(self, physician_id):
        # type: (int) -> Dict
        return self.request.get(self.url + str(physician_id) + '/')
