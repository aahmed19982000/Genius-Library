from django import forms
from .models import PaperColor , PaperType , PaperSize
class PaperColorForm(forms.ModelForm):
        class Meta:
          model = PaperColor
          fields = ['color_paper', 'price']

class PaperTypeForm(forms.ModelForm):
      class Meta:
           model = PaperType
           fields =['paper_type','price']

class PaperSizeForm(forms.ModelForm):
     class Meta:
          model = PaperSize
          fields =['size', 'price']