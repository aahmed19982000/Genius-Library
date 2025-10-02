from django.contrib import admin
from .models import Client
# Register your models here.

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("username", "first_name", "last_name", "email", "phone_number", "address")
    search_fields = ("username", "first_name", "last_name", "email", "phone_number")
    list_filter = ("address",)