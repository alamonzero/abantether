from decimal import Decimal

from django.conf import settings
import redis

from abantether.celery import app
from purchase.helpers.exchange_purchase import buy_from_exchange
from utils.redis_handler import RedisManager


@app.task(
    bind=True,
    name="buy_from_third_party_exchange",
    max_retries=settings.CELERY_MAX_RETRIES,
    retry_backoff=True,
    retry_backoff_max=settings.CELERY_RETRY_BACKOFF_MAX_IN_SECONDS,
    queue="buy_from_third_party_exchange",
)
def buy_from_third_party_exchange(self, currency: str, amount: float):
    try:
        purchase_was_successful = buy_from_exchange(currency, amount)
        if purchase_was_successful:
            return
        self.retry()
    except Exception as e:
        # NOTE:   we must log the exception here
        return


@app.task(name="fire_purchase_event")
def check_purchase_from_exchange_condition(
    currency: str, currency_price: Decimal, currency_new_amount: Decimal
):
    with RedisManager().client.pipeline() as pipe:
        while True:
            try:
                pipe.watch(currency)
                currency_current_amount = Decimal(pipe.get(currency).decode("utf8") or 0)
                total_price_of_queued_purchases = (
                    currency_current_amount * currency_price
                ) + (currency_new_amount * currency_price)
                currency_total_amount = currency_current_amount + currency_new_amount

                pipe.multi()
                if (
                    total_price_of_queued_purchases
                    >= settings.INTERNATIONAL_EXCHANGE_MINIMUM_BUY_AMOUNT
                ):
                    pipe.set(currency, 0)
                    buy_from_third_party_exchange.delay(currency, currency_total_amount)
                else:
                    pipe.set(currency, str(currency_total_amount))

                pipe.execute()
                break

            except redis.WatchError:
                continue
