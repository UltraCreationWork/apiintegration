from django.contrib import admin
from django.contrib.auth.models import Group
from .models import *
# Register your models here.
admin.site.site_header = "Trading Robot Admin v1.0"
admin.site.register(StockSymbolTable)
admin.site.register(StockExchange)
admin.site.unregister(Group)