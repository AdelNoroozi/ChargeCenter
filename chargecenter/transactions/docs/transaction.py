from drf_spectacular.utils import OpenApiParameter, OpenApiResponse

from chargecenter.transactions.serializers import TransactionPaginatedOutputSerializer

GET_TRANSACTIONS_PARAMETERS = [
    OpenApiParameter(name="page_size", description="must be a valid int"),
    OpenApiParameter(name="page", description="must be a valid int"),
    OpenApiParameter(name="created_at__gt", description="must be a valid date"),
    OpenApiParameter(name="created_at__lt", description="must be a valid date"),
    OpenApiParameter(name="updated_at__gt", description="must be a valid date"),
    OpenApiParameter(name="updated_at__lt", description="must be a valid date"),
    OpenApiParameter(name="amount", description="must be an integer"),
    OpenApiParameter(name="status", description="can be 'PND' (for pending transactions), 'DN' (for done transactions) "
                                                "& 'WTH' (for withdrawn transaction)"),
    OpenApiParameter(name="is_charge", description="must be true (for charge transactions) or false"
                                                   " (for balance transactions)"),
    OpenApiParameter(name="concrete_charge_obj__phone_number", description="must be a phone number or id of a "
                                                                           "phone number object"),
    OpenApiParameter(name="concrete_balance_obj__is_confirmed", description="must be true or false"),
    OpenApiParameter(name="concrete_balance_obj__confirmed_by", description="must id of an admin user, only accessible"
                                                                            " by admins"),
    OpenApiParameter(name="order_by", description="can be amount, created_at or updated_at. a - symbol can be added "
                                                  "before the param for descending order."),
]

GET_TRANSACTIONS_200_RESPONSE = OpenApiResponse(
    response=TransactionPaginatedOutputSerializer(),
    description="Represents a paginated list of transactions. If the requesting user is a salesperson it will only show"
                " the transactions that belong to that salesperson, otherwise all of the transactions will be returned."
                " The concrete object field can either be a charge transaction object or a balance transaction object "
                "based on the transaction type. Pay attention that the confirmed_by field inside balance transaction "
                "objects is only visible to admin users. Ordering and filtering the returning list is available using "
                "documented query parameters."
)

TRANSACTIONS_401_RESPONSE = OpenApiResponse(
    description="user is not authenticated"
)

GET_TRANSACTIONS_403_RESPONSE = OpenApiResponse(
    description="salesperson user is trying to filter (balance) transactions by their confirmed_by field."
)

GET_TRANSACTIONS_RESPONSES = {
    200: GET_TRANSACTIONS_200_RESPONSE,
    401: TRANSACTIONS_401_RESPONSE,
    403: GET_TRANSACTIONS_403_RESPONSE,
}