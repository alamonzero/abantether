from django.conf import settings
from utils.http_request_handler import HttpRequestHandler


def buy_from_exchange(crypto_title: str, amount: float) -> bool:
    request_handler = HttpRequestHandler(
        settings.BUY_FROM_EXCHANGE_REQUEST_ELEVATION,
        settings.BUY_FROM_EXCHANGE_REQUEST_DELAY,
        settings.BUY_FROM_EXCHANGE_REQUEST_MAX_RETRIES,
        settings.BUY_FROM_EXCHANGE_REQUEST_TIMEOUT,
    )
    data = {"currency": crypto_title, "amount": amount}
    status_code, response = request_handler.api_handler(
        settings.INTERNATIONAL_EXCHANGE_BUY_API_URL, "POST", data=data
    )
    #  NOTE:    log spot
    if 199 < status_code < 300:
        return True
    return False