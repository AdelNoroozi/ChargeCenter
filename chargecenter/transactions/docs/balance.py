from drf_spectacular.utils import OpenApiResponse

from chargecenter.transactions.serializers import TransactionOutputSerializer

CREATE_BALANCE_TRANSACTION_201_RESPONSE = OpenApiResponse(
    response=TransactionOutputSerializer(),
    description="A new balance transaction request is created by the authenticated user and will be applied on their "
                "balance after its confirmation by an admin user."
)

CREATE_BALANCE_TRANSACTIONS_400_RESPONSE = OpenApiResponse(
    description="input values are invalid or don't match the expected format. e.g: amount field is missing or its value"
                " is not a valid integer."
)

BALANCE_TRANSACTIONS_401_RESPONSE = OpenApiResponse(
    description="user is not authenticated"
)

CREATE_BALANCE_TRANSACTION_403_RESPONSE = OpenApiResponse(
    description="non salesperson user is trying to create a balance transaction."
)

CREATE_BALANCE_TRANSACTIONS_RESPONSES = {
    201: CREATE_BALANCE_TRANSACTION_201_RESPONSE,
    400: CREATE_BALANCE_TRANSACTIONS_400_RESPONSE,
    401: BALANCE_TRANSACTIONS_401_RESPONSE,
    403: CREATE_BALANCE_TRANSACTION_403_RESPONSE,
}


CONFIRM_BALANCE_TRANSACTION_200_RESPONSE = OpenApiResponse(
    description="used by admins to confirm a pending balance transaction and increase a salesperson's balance."
)

CONFIRM_BALANCE_TRANSACTIONS_400_RESPONSE = OpenApiResponse(
    description="input values are invalid or don't match the expected format. e.g: balance field is missing or is not a"
                " valid uuid."
)

CONFIRM_BALANCE_TRANSACTION_403_RESPONSE = OpenApiResponse(
    description="non admin user is trying to confirm a balance transaction."
)

CONFIRM_BALANCE_TRANSACTION_404_RESPONSE = OpenApiResponse(
    description="balance transaction with specified id not found."
)

CONFIRM_BALANCE_TRANSACTIONS_RESPONSES = {
    200: CONFIRM_BALANCE_TRANSACTION_200_RESPONSE,
    400: CONFIRM_BALANCE_TRANSACTIONS_400_RESPONSE,
    401: BALANCE_TRANSACTIONS_401_RESPONSE,
    403: CONFIRM_BALANCE_TRANSACTION_403_RESPONSE,
    404: CONFIRM_BALANCE_TRANSACTION_404_RESPONSE
}
