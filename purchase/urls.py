from django.urls import include, path

from purchase.views import PurchaseCryptoCurrency

urlpatterns = [
    path("crypto/", PurchaseCryptoCurrency.as_view(), name="purchase_crypto")
]