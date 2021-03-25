from django import forms
from .models import StockExchange,StockSymbolTable,PlaceOrder
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column,Field
from django.core import validators

stratgy = (
	("START1","START1"),
	("START2","START2"),
	("START3","START3"),
)

class OrderForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        helper = self.helper = FormHelper(self)
        layout = helper.layout = Layout()
        helper.form_show_labels = False




    # entryordertype = forms.CharField(label="")
    # exitordertype = forms.CharField(label="")
    quantity = forms.IntegerField(min_value=0)
    max_profit = forms.FloatField(min_value=0)
    max_loss = forms.FloatField(min_value=0)



    class Meta:
        model = PlaceOrder
        fields = ["exchange_symbol","input_symbol","exchange_name","instrumentname","entryordertype","exitordertype","quantity","product_type","max_profit","max_loss","strategy_tag"]
        widgets = {
        "exchange_symbol"   :       forms.TextInput(attrs={"placeholder":"Symbol","class":"basicAutoComplete", "data-url":"/data/"}),
        "input_symbol"      :       forms.TextInput(attrs={"placeholder":"InputSymbol"}),
        "instrumentname"    :       forms.TextInput(attrs={"placeholder":"InstrumentName"}),
        "quantity"          :       forms.NumberInput(attrs={"placeholder":"Quantity"}),
        "max_profit"        :       forms.NumberInput(attrs={"placeholder":"MaxProfit"}),
        "max_loss"          :       forms.NumberInput(attrs={"placeholder":"MaxLoss"}),

        }

