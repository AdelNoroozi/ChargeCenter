from django.urls import path

from chargecenter.phones.apis import PhoneNumbersAPI, PhoneNumberAPI

urlpatterns = [
    path("", PhoneNumbersAPI.as_view(), name='phone_numbers'),
    path("<str:id>", PhoneNumberAPI.as_view(), name='phone_number'),
]
