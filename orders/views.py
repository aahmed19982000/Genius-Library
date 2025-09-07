from django.shortcuts import render

# Create your views here.

def track_order(request):
    return render(request, 'orders/track_order.html')