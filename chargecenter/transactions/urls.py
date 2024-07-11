from django.urls import path

from chargecenter.transactions.apis import CreateBalanceTransaction

urlpatterns = [
    path('create-balance/', CreateBalanceTransaction.as_view(), name="create_balance")
]
