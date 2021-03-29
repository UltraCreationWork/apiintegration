from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
import random
import requests
from .models import *
from django.http import JsonResponse
import json
import pandas as pd
from nsetools import Nse
from django.conf import settings
from django.core.cache import cache
from .forms import OrderForm

def data(request):
	if request.is_ajax():
		q = request.GET.get('term', '')
		print(request.GET)
		print(q)
		data = StockSymbolTable.objects.filter(stock_symbols__istartswith=q)
		symbols = []
		for dt in data:
			symbols.append(dt.stock_symbols)
		return JsonResponse(symbols, safe=False)
	else:
		data = "failed to found"
		return JsonResponse(data, safe=False)

	


	# 	query = request.GET.get("term","")
	# if "term" in request.GET:
	# 	if query in cache:
	# 		context=cache.get(query)
	# 		symbols_cache = list()
	# 		for symbol in context:
	# 			symbols_cache.append(symbol.stock_symbols)
	# 		return JsonResponse(symbols_cache, safe=False)
	# 	else:
	# 		context = StockSymbolTable.objects.filter(stock_symbols__icontains=query)
	# 		symbols = list()
	# 		for symbol in context:
	# 			symbols.append(symbol.stock_symbols)
	# 		cache.set(symbol_name, context, timeout=settings.CACHE_TIMEOUT)	
	# 		return JsonResponse(symbols, safe=False)
		
def home(request):
	form = OrderForm(request.POST or request.GET or None)
	total_symbols_count = StockSymbolTable.objects.all().count()
	query = request.GET.get("exchange_symbol","")

	if request.is_ajax():
		q = request.GET.get('term', '')
		print(q)
		if q in request.GET.get('term', ''):
			data = StockSymbolTable.objects.filter(stock_symbols__istartswith=q)
			symbols = []
			for dt in data:
				symbols.append(dt.stock_symbols)
			return JsonResponse(symbols, safe=False)
		else:
			JsonResponse("failed to load data", safe=False)
	if request.method == "POST":
			if form.is_valid():
				print(form.data)
				form.save()
				return HttpResponse("success")
	return render(request,"index.html",{"form":form, "total_symbols_count": total_symbols_count})



def nse_index_quote(request):
	# if request.method=='POST':
	# 	q = nse.get_quote(request.POST.get('symbol'))
	# 	return JsonResponse(q, safe=False)
	q = nse.get_quote('BHARTIARTL')
	return JsonResponse(q, safe=False)

def nse_lot_size(request):
	data = nse.get_fno_lot_sizes()
	return JsonResponse(data, safe=False)


def order_history(request):
	return render(request,"order_history.html")

def trade_history(request):
	return render(request,"trade_history.html")



def signal(request):
	option = ["sell","buy"]
	signal = random.choice(option)
	color = "" 
	if signal == "buy":
		color = "#F3CDCD"
		data = {
		"color":color
		}
		return render(request,"signal.html",data)
	else:
		color = "#C7F2C8"
		data = {
		"color":color
		}
		return render(request,"signal.html",data)

def loginwithapi(request):
	return render(request,"api.html")

def signal_source(request):
	return render(request,"source.html")

def live_signal(request):
	option = ["sell","buy"]
	signal = random.choice(option)
	color = "" 
	if signal == "buy":
		color = "#F3CDCD"
		data = {
		"color":color
		}
		return render(request,"live.html",data)
	else:
		color = "#C7F2C8"
		data = {
		"color":color
		}
		return render(request,"live.html",data)





def database(request):
	# json_data = open(str(settings.BASE_DIR) + 'stock_name_symbols.json')
	json_data = open('stock_name_symbols.json')
	data1 = json.load(json_data)
	data2 = json.dumps(data1)
	NSE=StockExchange.objects.get(id=1)
	for key, value in data1.items():
		i = StockSymbolTable.objects.create(stock_name=value, stock_symbols=key)
		i.stock_exchange.add(NSE)
		print("completed")
	return JsonResponse("all data inserted", safe=False)
