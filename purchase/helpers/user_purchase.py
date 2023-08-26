from decimal import Decimal

from django.db import transaction

from user.models import User
from account.models import CryptoAccount, WalletAccount
from crypto_currency.models import CryptoCurrency
from purchase.tasks.buy_from_third_party_exchange import (
    check_purchase_from_exchange_condition,
)


def register_user_crypto_purchase(
    user: User, currency: CryptoCurrency, amount: Decimal
) -> tuple[bool, dict[str, str]]:
    total_price = Decimal(currency.price) * amount
    with transaction.atomic():
        wallet_account = WalletAccount.objects.select_for_update().get(user=user)
        crypto_account = CryptoAccount.custom_objects.select_for_update().get(
            user=user
        )
        if total_price < wallet_account.balance:
            wallet_account.balance -= total_price
            crypto_account.balance += amount
            wallet_account.save()
            crypto_account.save()
            check_purchase_from_exchange_condition.delay(currency.title, currency.price, amount)
            return True, {"error": "", "message": "Purchase was successful"}
        return False, {"error": "Insufficient funds", "message": ""}

