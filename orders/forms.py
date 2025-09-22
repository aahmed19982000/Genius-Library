from django import forms
from .models import Order


class UploadForm(forms.Form):
    file = forms.FileField(label='اختر الملف')

class OrderForm(forms.ModelForm):
    class Meta:
        model=Order
        fields = [
            'customer_name',
            'file_name',
            'paper_type',
            'paper_size',
            'printing_color',
            'printing_sides',
            'quantity',
            'address',
        ]