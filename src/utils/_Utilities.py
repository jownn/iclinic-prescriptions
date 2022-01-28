import os
from datetime import timedelta
from time import sleep
from typing import Any, Dict, Callable

from dotenv import load_dotenv
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import requests_cache

from src.model.exceptions import get_exception


def load_env():
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    load_dotenv(os.path.join(base_dir, ".env"))


def execute(trying_to_do, is_success, success, failed, sleep_seconds):
    # type: (Callable, Callable, Callable, Callable, int) -> Dict
    response = trying_to_do()
    if is_success(response):
        return success(response)
    else:
        failed(response)
    sleep(sleep_seconds)


def failed_responses(service: int, resp: requests.Response):
    get_exception(service=service, status_code=resp.status_code, raise_error=True)


class Request:
    def __init__(
            self,
            service,
            auth_token,
            cache_minutes=5,
            timeout=2,
            retries=2,
            session=None
    ):
        # type: (int, str, int, int, int, Any) -> None
        self.service = service
        self.timeout = timeout
        self.auth_token = auth_token
        self.headers = {'Authorization': self.auth_token, 'Content-Type': 'application/json'}
        if session:
            self.session = session
        elif cache_minutes:
            self.session = requests_cache.CachedSession(str(service), expire_after=timedelta(minutes=cache_minutes))
        else:
            self.session = requests.Session()

        retry = Retry(
            total=retries,
            read=retries,
            connect=retries,
            backoff_factor=0.3,
            status_forcelist=(500, 502, 504)
        )
        adapter = HTTPAdapter(max_retries=retry)
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)

    def get(self, url, params=None):
        # type: (str, Dict or None) -> Dict
        return execute(
            trying_to_do=lambda: self.session.get(url=url, headers=self.headers, timeout=self.timeout, params=params),
            is_success=lambda resp: resp.ok,
            success=lambda resp: resp.json(),
            failed=lambda resp: failed_responses(service=self.service, resp=resp),
            sleep_seconds=5
        )

    def post(self, url, data):
        # type: (str, Dict) -> Dict
        return execute(
            trying_to_do=lambda: self.session.post(url=url, headers=self.headers, timeout=self.timeout, json=data),
            is_success=lambda resp: resp.ok,
            success=lambda resp: resp.json(),
            failed=lambda resp: failed_responses(service=self.service, resp=resp),
            sleep_seconds=5
        )
