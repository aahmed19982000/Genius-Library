from django.shortcuts import render


def home_view(request):
    return render(request, 'home/index.html')


def contact(request):
    return render(request, 'home/contact.html')