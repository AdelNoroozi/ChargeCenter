from django.urls import path

from chargecenter.phones.apis import PhoneNumbersAPI

urlpatterns = [
    path("", PhoneNumbersAPI.as_view(), name='phone_numbers'),
]
