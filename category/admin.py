from django.contrib import admin
from .models import PaperColor , PaperType , PaperSize

# Register your models here.
@admin.register(PaperColor)
class PaperColorAdmin(admin.ModelAdmin):
    list_display = ("color_paper", "price")

@admin.register(PaperType)
class PaperTypeAdmin(admin.ModelAdmin):
    list_display = ("paper_type", "price")

@admin.register(PaperSize)
class PaperSizeAdmin(admin.ModelAdmin):
    list_display = ("size", "price")
