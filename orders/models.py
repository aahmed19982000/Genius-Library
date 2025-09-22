from django.db import models

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'قيد الانتظار'),
        ('inprogress', 'جاري التنفيذ'),
        ('done', 'تم التنفيذ'),
    ]
    COLOR_CHOICES = [
        ('black and white', 'ابيض واسود'),
        ('colored', 'الوان'),
    ]

    PAPER_SIZE=[
        ('A4','A4'),
        ('A3','A3'),
        ('A2','A2'),
]
    
    PAPER_TYPE=[
        ('plain paper','عادي'),
        ('glossy paper','لمع'),
        ('sticky paper','لاصق'),
        ('cardboard','مقوى'),
        ]
    PAPER_SIDES=[
        ('one side','وجه واحد'),
        ('tow side','وجهين'),

]
    

    customer_name = models.CharField(max_length=100, verbose_name="اسم العميل")
    file_name = models.FileField(upload_to="uploads/", verbose_name="الملف") 
    paper_type = models.CharField(max_length=50,choices=PAPER_TYPE,default='plain paper', verbose_name="نوع الورق")
    paper_size = models.CharField(max_length=50, choices=PAPER_SIZE, default='A4', verbose_name="حجم الورق")
    printing_color = models.CharField(max_length=20, choices=COLOR_CHOICES,default='black and white', verbose_name="لون الطباعة")
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
