from django.db import models
from category.models import PaperColor, PaperType, PaperSize , Status
from django.contrib.auth.models import User
from clients.models import Client
from django.conf import settings  # لو هتستخدم نظام المستخدمين الافتراضي

class Order(models.Model):
 

    PAPER_SIDES=[
        ('one side','وجه واحد'),
        ('tow side','وجهين'),

]
    
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="orders")  
    customer_name = models.CharField(max_length=100, verbose_name="اسم العميل")
    file_name = models.FileField(upload_to="uploads/", verbose_name="الملف") 
    paper_type = models.ForeignKey(PaperType, on_delete=models.CASCADE, verbose_name="نوع الورق")
    paper_size = models.ForeignKey(PaperSize, on_delete=models.CASCADE, verbose_name="حجم الورق")
    printing_color =  models.ForeignKey(PaperColor, on_delete=models.CASCADE, verbose_name="لون الطباعة")
    printing_sides = models.CharField(max_length=20, choices=PAPER_SIDES,default='one side', verbose_name="الطباعة على وجه /وجهين")
    number_of_sheets= models.PositiveIntegerField(verbose_name="عدد الاوراق")
    quantity = models.PositiveIntegerField(verbose_name="عدد النسخ")
    address = models.CharField(max_length=255, verbose_name="العنوان")
    notes = models.TextField(null=True, blank=True)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="إجمالي التكلفة")
    status =  models.ForeignKey(Status, on_delete=models.CASCADE, verbose_name="الحالة")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الطلب")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاريخ آخر تعديل")

    def __str__(self):
        return f"{self.customer_name} - {self.file_name} ({self.status})"



class OrderChat(models.Model):
    order = models.ForeignKey("Order", on_delete=models.CASCADE, related_name="chats")  
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sent_messages")  
    message = models.TextField(verbose_name="الرسالة")
    file = models.FileField(upload_to="chat_files/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإرسال")
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.sender} - {self.order}"
