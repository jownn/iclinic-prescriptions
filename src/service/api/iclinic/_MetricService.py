from typing import Dict

from src.model.requests import MetricRequest
from src.utils import Request


class MetricService:
    def __init__(self, url, auth_token):
        self.url = url
        self.auth_token = auth_token
        self.request = Request(5, auth_token=self.auth_token, cache_minutes=0, timeout=6, retries=5)

    def post(self, metric):
        # type: (MetricRequest) -> Dict
        return self.request.post(self.url, metric.__dict__)
