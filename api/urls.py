from django.urls import path, include

urlpatterns = [
    path('auth/', include('clients.api.urls')),
    path('home/', include('home.api.urls')),
    path('orders/', include('orders.api.urls')),
]