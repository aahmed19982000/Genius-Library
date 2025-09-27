from django.urls import path
from . import views

urlpatterns = [
    path('colors/', views.paper_colors, name='paper_colors'),
    path('paper_types/', views.paper_types, name='paper_types'),
    path('papersize/', views.papersize, name='papersize'),
   ]