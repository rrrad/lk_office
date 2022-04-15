from django.contrib import admin
from .models import Order, Invoice, Act

admin.site.register(Order)
admin.site.register(Invoice)
admin.site.register(Act)