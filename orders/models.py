from django.db import models
from category.models import PaperColor, PaperType, PaperSize

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'قيد الانتظار'),
        ('inprogress', 'جاري التنفيذ'),
        ('done', 'تم التنفيذ'),
    ]

    PAPER_SIDES=[
        ('one side','وجه واحد'),
        ('tow side','وجهين'),

]
    

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
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="الحالة")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الطلب")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاريخ آخر تعديل")

    def __str__(self):
        return f"{self.customer_name} - {self.file_name} ({self.status})"
