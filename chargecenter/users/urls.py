from django.urls import path

from chargecenter.users.apis import CreateAdminAPI

urlpatterns = [
    path('add-admin/', CreateAdminAPI.as_view(), name="add_admin")
]
