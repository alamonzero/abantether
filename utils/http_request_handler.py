import time
import requests
from urllib3 import Retry


class HttpRequestHandler:
    def __init__(
        self, elevation: int, delay: int, number_of_retries: int, timeout: int
    ):
        super(HttpRequestHandler, self).__init__()
        self.elevation = elevation
        self.delay = delay
        self.number_of_retries = number_of_retries
        self.timeout = timeout

    def __send_request(self, data: dict | None, url: str, method: str, headers: dict):
        session = requests.Session()
        adaptor = requests.adapters.HTTPAdapter(
            max_retries=Retry(
                total=self.number_of_retries,
                backoff_factor=self.delay,
                allowed_methods=None,
                status_forcelist=[429, 500, 502, 503, 504, 507],
            )
        )
        session.mount("http", adaptor)
        session.mount("https", adaptor)
        response = session.request(
            method, url, json=data, headers=headers, timeout=self.timeout, verify=False
        )
        return response

    def api_handler(
        self, url: str, method: str, data: dict | None = None, headers: dict = {}
    ) -> tuple[int, str]:
        current_request_try: int = 0
        current_request_delay: int = self.delay
        response = None
        while current_request_try < self.number_of_retries:
            try:
                response = self.__send_request(data, url, method, headers)
                return response.status_code, response.text
            except (
                requests.exceptions.ConnectTimeout,
                requests.exceptions.ConnectionError,
            ):
                time.sleep(current_request_delay)
                current_request_try += 1
                current_request_delay += self.elevation
            except requests.exceptions.RetryError:
                pass
        return 504, '{"error": "Gateway Timeout"}'
