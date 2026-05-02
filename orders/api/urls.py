from django.urls import path
from .views import PaperOptionsView, OrderCreateView, ClientOrderListView , CountPagesView

urlpatterns = [
    path('options/', PaperOptionsView.as_view(), name='paper_options'),
    path('count-pages/', CountPagesView.as_view(), name='count-pages'),
    path('create/', OrderCreateView.as_view(), name='order_create'),
    path('my-orders/', ClientOrderListView.as_view(), name='client_orders'),
]