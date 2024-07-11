from django.urls import path

from chargecenter.transactions.apis import CreateBalanceTransactionAPI, ConfirmBalanceTransactionAPI

urlpatterns = [
    path('create-balance/', CreateBalanceTransactionAPI.as_view(), name="create_balance"),
    path('confirm-balance/', ConfirmBalanceTransactionAPI.as_view(), name="confirm_balance"),
]
