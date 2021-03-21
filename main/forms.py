from django import forms
from .models import StockExchange,StockSymbolTable
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column,Field

class StockForm(forms.ModelForm):
    stock_symbols = forms.CharField(label='')
    class Meta:
        model = StockSymbolTable
        fields = ["stock_symbols"]
        widgets = {
        'stock_symbols': forms.TextInput(attrs={'placeholder':'Symbol'}),
        }

