from django.urls import path, include

urlpatterns = [
    path('users/', include('chargecenter.users.urls')),
    path('auth/', include('chargecenter.authentication.urls')),
    path('transaction/', include('chargecenter.transactions.urls')),
]
