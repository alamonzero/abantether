from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from purchase.serializers import PurchaseCryptoCurrencySerializer
from purchase.helpers.user_purchase import register_user_crypto_purchase


class PurchaseCryptoCurrency(APIView):
    def post(self, request):
        raw_data = PurchaseCryptoCurrencySerializer(data=request.data)
        raw_data.is_valid(raise_exception=True)
        valid_and_serialized_data = raw_data.validated_data
        was_successful, response_content = register_user_crypto_purchase(
            request.user,
            valid_and_serialized_data["crypto_currency"],
            valid_and_serialized_data["amount"],
        )
        response_status_code = status.HTTP_400_BAD_REQUEST
        if was_successful:
            response_status_code = status.HTTP_200_OK
        return Response(data=response_content, status=response_status_code)