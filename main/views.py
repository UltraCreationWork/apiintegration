from django.shortcuts import render
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

def home(request):
	symbol=""
	if symbol in cache:
		context = cache.get(symbol)
		print("getting context from cache --->",context)
		return render(request,"index.html",context)
	else:
		symbols = StockSymbolTable.objects.all().count()
		context = {
			"total_symbols_count": symbols,

		}
		print("getting context from db --->",context)
		cache.set(symbol, context, timeout=settings.CACHE_TIMEOUT)
		return render(request,"index.html", context)


def get_stock_details_by_symbol(request):
	symbol_name = request.GET.get('q')
	if symbol_name in request.GET:
		if symbol_name in cache:
			context=cache.get(symbol_name)
			print("getting context from cache --->",context)
			return JsonResponse(context, safe=False)
		else:
			context = StockSymbolTable.objects.filter(stock_symbols=symbol_name)
			print("getting context from db --->",context)
			cache.set(symbol_name, context, timeout=settings.CACHE_TIMEOUT)
			return JsonResponse(context, safe=False)

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




