from django.contrib import admin
from .models import Order

# تسجيل الموديل علشان يظهر في لوحة التحكم
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("customer_name", "file_name", "paper_type", "quantity", "address", "status","printing_color","paper_size")
    search_fields = ("customer_name", "file_name", "address")
    list_filter = ("status", "paper_type")
