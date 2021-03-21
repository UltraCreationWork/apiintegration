from django.contrib import admin
from django.contrib.auth.models import Group
from .models import *
# Register your models here.
admin.site.site_header = "Trading Robot Admin v1.0"
admin.site.register(StockExchange)
admin.site.unregister(Group)

class StockSymbolTableAdmin(admin.ModelAdmin):
    list_display = ('stock_name', 'stock_symbols', 'get_stock_exchanges')
    fields = (
        'stock_name',
        'stock_symbols',
        'stock_exchange',
        )

admin.site.register(StockSymbolTable, StockSymbolTableAdmin)

class PlaceOrderAdmin(admin.ModelAdmin):
    list_display = ('order_id','date_time','exchange_symbol')
    fields = (
        'order_id',
        'date_time',
        'exchange_symbol',
        )
admin.site.register(PlaceOrder, PlaceOrderAdmin)