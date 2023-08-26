from django.db import models

from base.models import TimestampBaseModel, SoftDeleteModel
from crypto_currency.constants import CryptoCurrencyTitleChoices




class CryptoCurrency(TimestampBaseModel, SoftDeleteModel):
    title = models.CharField(
        max_length=128,
        null=False,
        blank=False,
        choices=CryptoCurrencyTitleChoices.choices,
    )
    logo = models.URLField(blank=False, null=False)
    price = models.DecimalField(max_digits=20, null=False, decimal_places=10)
