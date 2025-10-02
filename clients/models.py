from django.db import models
from django.contrib.auth.models import AbstractUser


USER_TYPE_CHOICES = (
    ('client', 'عميل'),
    ('admin', 'أدمن'),
)


# Create your models here.
class Client(AbstractUser):
    phone_number = models.CharField(max_length=15, verbose_name="رقم الهاتف", blank=True, null=True)
    address = models.CharField(max_length=255, verbose_name="العنوان", blank=True, null=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='client')

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.username}"