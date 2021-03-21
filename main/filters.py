import django_filters
from .models import StockExchange

class StockFilter(django_filters.FilterSet):
    exchange_name = django_filters.CharFilter(lookup_expr="icontains")
    class Meta:
        model = StockExchange
        fields = "__all__"