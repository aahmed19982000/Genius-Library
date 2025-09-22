from django.shortcuts import render
from orders.models import Order

# وظيفة لوحوة التحكم
def dashboard(request):
    return render(request,  'bakend/dashboard.html')

#وظيفة عرض الرسائل في لوحة التحكم 
def messages(request):
    return render(request,  'bakend/messages.html')

#وظيفة عرض الطلبات في لوحة التحكم 
def orders(request):
    orders = Order.objects.all()

    return render(request, 'bakend/orders.html',{"orders": orders})
