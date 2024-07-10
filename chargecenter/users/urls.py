from django.urls import path

from chargecenter.users.apis import CreateAdminAPI, CreateSalesPersonAPI

urlpatterns = [
    path('add-admin/', CreateAdminAPI.as_view(), name="add_admin"),
    path('add-salesperson/', CreateSalesPersonAPI.as_view(), name="add_salesperson")
]
