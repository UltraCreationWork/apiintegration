from django.db import models
from django.db.models import Model as M
from .utils import unique_order_id_generator
from django.db.models.signals import pre_save
import enum

# from django_postgres_extensions.models.fields import ArrayField
# Create your models here.
class TransactionType(enum.Enum):
    Buy = 'BUY'
    Sell = 'SELL'

class OrderType(enum.Enum):
    Market = 'MARKET'
    Limit = 'LIMIT'
    StopLossLimit = 'SL'
    StopLossMarket = 'SL-M'

class ProductType(enum.Enum):
    Intraday = 'I'
    Delivery = 'D'
    CoverOrder = 'CO'
    BracketOrder = 'BO'

class StockExchange(M):
	exchange_name = models.CharField(max_length=20, verbose_name="Exchange Name")

	class Meta:
		verbose_name_plural = 'StockExchanges'
		ordering = ['-exchange_name']
		
	def __str__(self):
		return self.exchange_name

	def __unicode__(self):
	   return self.exchange_name

	def serialize(self):
		return {
			"id": self.id,
			"exchange name": self.exchange_name
		}


class StockSymbolTable(M):
	stock_name = models.CharField(max_length=200, verbose_name="Stock Name", null=True, blank=True)
	stock_symbols = models.CharField(max_length=20, verbose_name="Stock Symbols")
	stock_exchange = models.ManyToManyField(StockExchange,related_name="StockExchanges")
	# stock_exchange = ArrayField(models.CharField(max_length=20), null=True, blank=True)

	class Meta:
		verbose_name_plural = 'StockSymbolTables'
		ordering = ['-stock_name']
		
	def __str__(self):
		return self.stock_symbols

	def serialize(self):
		return {
			"id": self.id,
			"stock name": self.stock_name,
			"stock symbols": self.stock_symbols
		}

	def get_stock_exchanges(self):
		return "\n".join([str(p) for p in self.stock_exchange.all()])


type_=(
	("Market","Market"),
)

stratgy = (
	("START1","START1"),
	("START2","START2"),
	("START3","START3"),
)

order_type = (
	("MARKET","Market"),
	("LIMIT","Limit"),
	("SL","StopLossLimit"),
	("SL-M","StopLossMarket"),
	)
product_type = (
	("I","Intraday"),
	("D","Delivery"),
	("CO","CoverOrder"),
	("BO","BracketOrder"),
	)
transaction_type = (
	("BUY","Buy"),
	("SELL","Sell"),
	)

 




class PlaceOrder(M):
	transaction_type = models.CharField(choices=transaction_type,max_length=50,verbose_name="TransactionType")
	order_id  = models.CharField(max_length=120,blank=True,unique=True)
	alice_blue_order_id = models.CharField(max_length=200,blank=True,verbose_name="alice_blue_order_id")
	exchange_symbol = models.CharField(max_length=20,verbose_name="ExChange Symbol")
	input_symbol = models.CharField(max_length=20,verbose_name="Input Symbol")
	exchange_name = models.CharField(max_length=15,verbose_name="ExChange",choices=(
		("NSE","NSE"),
		("BSE","BSE"),
		("MCX","MCX"),
		("FUTURE OPTION","FUTURE OPTION")))
	instrumentname = models.CharField(max_length=20,verbose_name="InstrumentName")
	ordertype = models.CharField(choices=order_type,max_length=50,verbose_name="OrederType")
	quantity = models.PositiveIntegerField(verbose_name="Quantity")
	product_type = models.CharField(choices=product_type,max_length=50,verbose_name="PoductType")
	max_profit = models.FloatField(verbose_name="Maximum Profit")
	max_loss = models.FloatField(verbose_name="Maximum Loss")
	strategy_tag = models.CharField(max_length=50,choices=stratgy,verbose_name="StrategyTag")
	date_time = models.DateTimeField(auto_now_add=True,verbose_name="Date of Order")

	def __unicode__(self):
		return self.order_id
	
	class Meta:
		ordering = ["-date_time"]

def pre_save_create_order_id(sender, instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id= unique_order_id_generator(instance)


pre_save.connect(pre_save_create_order_id, sender=PlaceOrder)
