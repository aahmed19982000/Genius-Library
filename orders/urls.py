from django.contrib import admin
from django.urls import path
from views import  track_order 
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', track_order, name='track_order'),   
]
