from django.db import models

# Create your models here. 
class PaperColor(models.Model):
    color_paper = models.CharField(max_length=50, verbose_name="لون الورق")
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="السعر")

    def __str__(self):
        return self.color_paper


class PaperType(models.Model):
    paper_type = models.CharField(max_length=100, verbose_name="نوع الورق")
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="السعر")

    def __str__(self):
        return self.paper_type

class PaperSize(models.Model):
    size = models.CharField(max_length=50, verbose_name="حجم الورق")
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="السعر")

    def __str__(self):
        return self.size