from rest_framework import serializers

from crypto_currency.models import CryptoCurrency


class PurchaseCryptoCurrencySerializer(serializers.Serializer):
    crypto_currency = serializers.SlugRelatedField(
        slug_field="title",
        queryset=CryptoCurrency.custom_objects.all(),
        required=True,
        allow_null=False,
    )
    amount = serializers.DecimalField(max_digits=20, decimal_places=10, required=True, allow_null=False)
