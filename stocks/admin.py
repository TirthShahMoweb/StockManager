from django.contrib import admin

from .models import product, stockEntry, stockBunch

admin.site.register(product)
admin.site.register(stockEntry)
admin.site.register(stockBunch)