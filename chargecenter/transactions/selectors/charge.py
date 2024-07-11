from chargecenter.transactions.models import Transaction, ChargeTransaction


def create_charge(transaction: Transaction, phone_number: str):
    return ChargeTransaction.objects.create(transaction_obj=transaction, phone_number=phone_number)