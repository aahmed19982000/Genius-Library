from django.shortcuts import render
from orders.models import Order , OrderChat
from category.models import Status
from clients.decorators import role_required



@role_required(allowed_roles=['admin'])
def dashboard(request):
    orders = Order.objects.all().order_by('-created_at')[:10]
    unread_messages = OrderChat.objects.filter(is_read=False).exclude(sender=request.user).order_by ('-created_at') [:10]
    all_status = Status.objects.all()

    context = {
        'orders': orders,
        'unread_messages': unread_messages,
        'all_status': all_status,
    }

    return render(request, 'bakend/dashboard.html', context)

#وظيفة عرض الرسائل في لوحة التحكم 
@role_required(allowed_roles=['admin'])
def messages(request):
    return render(request,  'bakend/messages.html')

#وظيفة عرض الطلبات في لوحة التحكم 
@role_required(allowed_roles=['admin'])
def orders(request):
    orders = Order.objects.all().order_by('-created_at')
    all_status = Status.objects.all()

    return render(request, 'bakend/orders.html',{
        "orders": orders,
        "all_status": all_status
        
        })
