from chargecenter.transactions.filters import TransactionFilter
from chargecenter.transactions.selectors import get_transactions as get_transactions_selector
from chargecenter.transactions.serializers import TransactionOutputSerializer
from chargecenter.users.models import BaseUser


def get_transactions(user: BaseUser, query_dict: dict):
    transactions = get_transactions_selector(return_all=user.is_admin,
                                             salesperson=user.salesperson if not user.is_admin else None)
    transactions = TransactionFilter(query_dict, queryset=transactions).qs
    serializer = TransactionOutputSerializer(transactions, many=True, context={"full_access": user.is_admin})
    return serializer.data
