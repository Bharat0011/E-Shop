from django.contrib import admin
from . import models

class AdminProduct(admin.ModelAdmin):
    list_display = ['name', 'price', 'category']

class AdminCategory(admin.ModelAdmin):
    list_display = ['name']

admin.site.register(models.Product, AdminProduct)
admin.site.register(models.Category, AdminCategory)
admin.site.register(models.Customer)
admin.site.register(models.Order)
