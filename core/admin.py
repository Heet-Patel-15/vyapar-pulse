from django.contrib import admin
from .models import Business, Product, TransactionRecord

admin.site.register(Business)
admin.site.register(Product)
admin.site.register(TransactionRecord)