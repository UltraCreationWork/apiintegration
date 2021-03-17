from django.db import models
from django.db.models import Model as M

# from django_postgres_extensions.models.fields import ArrayField
# Create your models here.
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




