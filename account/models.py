from django.db import models

from base.models import TimestampBaseModel, SoftDeleteModel, SoftDeleteCustomManager
from crypto_currency.models import CryptoCurrency
from user.models import User


class CryptoAccountCustomManager(SoftDeleteCustomManager):
    def get_queryset(self) -> models.query.QuerySet:
        return super().get_queryset().select_related("user")


class CryptoAccount(TimestampBaseModel, SoftDeleteModel):
    crypto_currency = models.ForeignKey(
        CryptoCurrency, on_delete=models.PROTECT, null=False, related_name="accounts"
    )
    user = models.ForeignKey(
        User, on_delete=models.PROTECT, null=False, related_name="crypto_accounts"
    )
    balance = models.DecimalField(
        max_digits=20, decimal_places=10, null=False, default=0
    )
    number = models.BigIntegerField(null=False, db_index=True)
    custom_objects = CryptoAccountCustomManager()

    class Meta:
        unique_together = ('crypto_currency', 'user')


class WalletAccountCustomManager(models.Manager):
    def get_queryset(self) -> models.query.QuerySet:
        return super().get_queryset().select_related("user")


class WalletAccount(TimestampBaseModel):
    user = models.OneToOneField(
        User, on_delete=models.PROTECT, null=False, related_name="wallet_account"
    )
    balance = models.DecimalField(
        max_digits=20, decimal_places=10, null=False, default=0
    )
    number = models.BigIntegerField(null=False, db_index=True)
    custom_objects = WalletAccountCustomManager()
