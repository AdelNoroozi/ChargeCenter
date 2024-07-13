from drf_spectacular.utils import OpenApiResponse

from chargecenter.transactions.serializers import TransactionOutputSerializer

CREATE_CHARGE_TRANSACTION_201_RESPONSE = OpenApiResponse(
    response=TransactionOutputSerializer(),
    description="A new charge transaction request is created by the authenticated user, a request to an external "
                "charging service is made and the transactions amount is reduced from salesperson's balance."
)

CREATE_CHARGE_TRANSACTIONS_400_RESPONSE = OpenApiResponse(
    description="input values are invalid or don't match the expected format. e.g: amount field is missing or its value"
                " is not a valid integer/ phone_number field is missing or its value is not a valid uuid."
)

CHARGE_TRANSACTIONS_401_RESPONSE = OpenApiResponse(
    description="user is not authenticated"
)

CREATE_CHARGE_TRANSACTION_403_RESPONSE = OpenApiResponse(
    description="non salesperson user is trying to create a charge transaction."
)

CREATE_CHARGE_TRANSACTION_404_RESPONSE = OpenApiResponse(
    description="phone number with specified id not found."
)

CREATE_CHARGE_TRANSACTIONS_RESPONSES = {
    201: CREATE_CHARGE_TRANSACTION_201_RESPONSE,
    400: CREATE_CHARGE_TRANSACTIONS_400_RESPONSE,
    401: CHARGE_TRANSACTIONS_401_RESPONSE,
    403: CREATE_CHARGE_TRANSACTION_403_RESPONSE,
    404: CREATE_CHARGE_TRANSACTION_404_RESPONSE
}
