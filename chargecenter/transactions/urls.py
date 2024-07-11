from django.urls import path

from chargecenter.transactions.apis import CreateBalanceTransactionAPI, ConfirmBalanceTransactionAPI, \
    CreateChargeTransactionAPI

urlpatterns = [
    path('create-balance/', CreateBalanceTransactionAPI.as_view(), name="create_balance"),
    path('create-charge/', CreateChargeTransactionAPI.as_view(), name="create_charge"),
    path('confirm-balance/', ConfirmBalanceTransactionAPI.as_view(), name="confirm_balance"),
]
