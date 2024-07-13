from chargecenter.common.validators import is_valid_uuid
from chargecenter.phones.models import PhoneNumber
from chargecenter.transactions.filters import TransactionFilter
from chargecenter.transactions.selectors import get_transactions as get_transactions_selector, order_transactions
from chargecenter.transactions.serializers import TransactionOutputSerializer
from chargecenter.users.models import BaseUser


def get_transactions(user: BaseUser, query_dict: dict):
    transactions = get_transactions_selector(return_all=user.is_admin,
                                             salesperson=user.salesperson if not user.is_admin else None)
    local_query_dict = query_dict.copy()
    order_param = local_query_dict.get('order_by')
    if order_param and order_param.lstrip("-") in ["amount", "created_at", "updated_at"]:
        transactions = order_transactions(queryset=transactions, order_param=order_param)
    if is_valid_uuid(val=local_query_dict.get("concrete_charge_obj__phone_number")):
        phone_number = PhoneNumber.objects.filter(id=local_query_dict.get("concrete_charge_obj__phone_number")).first()
        if phone_number:
            local_query_dict["concrete_charge_obj__phone_number"] = phone_number.number
    transactions = TransactionFilter(local_query_dict, queryset=transactions).qs
    serializer = TransactionOutputSerializer(transactions, many=True, context={"full_access": user.is_admin})
    return serializer.data
