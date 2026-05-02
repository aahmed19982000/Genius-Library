from django.urls import path
from .views import (
    APILoginView, APISignupView, APIEmployeeListView, 
    APIEmployeeDeleteView, APINotificationListView, APINotificationActionView
)

urlpatterns = [
    path('login/', APILoginView.as_view(), name='api_login'),
    path('signup/', APISignupView.as_view(), name='api_signup'),
    path('employees/', APIEmployeeListView.as_view(), name='api_employee_list'),
    path('employees/<int:id>/delete/', APIEmployeeDeleteView.as_view(), name='api_employee_delete'),
    path('notifications/', APINotificationListView.as_view(), name='api_notifications'),
    path('notifications/<int:pk>/<str:action>/', APINotificationActionView.as_view(), name='api_notification_action'),
]