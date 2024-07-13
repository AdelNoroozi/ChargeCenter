from django.urls import path, include

urlpatterns = [
    path('users/', include('chargecenter.users.urls')),
    path('auth/', include('chargecenter.authentication.urls')),
    path('transactions/', include('chargecenter.transactions.urls')),
    path('phone-numbers/', include('chargecenter.phones.urls')),
]
