from django.contrib import admin
from django.urls import path
from .views import dashboard , messages , orders
from category import views as category_views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', dashboard, name='dashboard'), 
    path('messages/', messages, name='messages'),
    path('orders/', orders, name='orders'),
    path('paper_colors/', category_views.paper_colors, name='paper_colors'),  
    path('paper_types/', category_views.paper_types, name='paper_types'),  
    
    ]