from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Client


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = Client
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "address",
            "password1",
            "password2",
        ]
        labels = {
            "username": "اسم المستخدم",
            "first_name": "الاسم الأول",
            "last_name": "اسم العائلة",
            "email": "البريد الإلكتروني",
            "phone_number": "رقم الهاتف",
            "address": "العنوان",
            "password1": "كلمة المرور",
            "password2": "تأكيد كلمة المرور",
        }
