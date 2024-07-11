from chargecenter.transactions.models import Transaction, BalanceTransaction


def create_balance(transaction: Transaction):
    return BalanceTransaction.objects.create(transaction_obj=transaction)
