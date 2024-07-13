from django_filters.rest_framework import FilterSet

from chargecenter.transactions.models import Transaction


class TransactionFilter(FilterSet):
    class Meta:
        model = Transaction
        fields = {
            "created_at": ["lt", "gt"],
            "updated_at": ["lt", "gt"],
            "amount": ["lt", "gt"],
            "status": ["exact"],
            "is_charge": ["exact"],
            "salesperson": ["exact"],
            "concrete_charge_obj__phone_number": ["exact"],
            "concrete_balance_obj__is_confirmed": ["exact"],
            "concrete_balance_obj__confirmed_by": ["exact"]
        }
