from django.urls import path
from . import views

urlpatterns = [
    path('', views.track_order, name='track_order'), 
    path('upload/', views.upload_file, name='upload_file'),
    path('choose_paper/', views.choose_paper, name='choose_paper'),
    path('delivery_details/', views.delivery_details , name='delivery_details'),
    path('payment_and_confirmation/', views.payment_and_confirmation , name='payment_and_confirmation'),
    path('thank_you/', views.thank_you , name='thank_you'),
    path("order/<int:order_id>/chat/", views.orderchat, name="orderchat"),
    path("order/<int:order_id>/", views.order_detail, name="order_detail"),


]
