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
from tradingview_ta import TA_Handler, Interval, Exchange
from alice_blue import *
from .constants import (alice_blue_login, alice_blue_object)

# from nsetools import Nse
import nse50bse30
# nse = Nse()

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

	


	#   query = request.GET.get("term","")
	# if "term" in request.GET:
	#   if query in cache:
	#       context=cache.get(query)
	#       symbols_cache = list()
	#       for symbol in context:
	#           symbols_cache.append(symbol.stock_symbols)
	#       return JsonResponse(symbols_cache, safe=False)
	#   else:
	#       context = StockSymbolTable.objects.filter(stock_symbols__icontains=query)
	#       symbols = list()
	#       for symbol in context:
	#           symbols.append(symbol.stock_symbols)
	#       cache.set(symbol_name, context, timeout=settings.CACHE_TIMEOUT) 
	#       return JsonResponse(symbols, safe=False)
		
def home(request):
	form = OrderForm(request.POST or request.GET or None)
	total_symbols_count = StockSymbolTable.objects.all().count()
	query = request.GET.get("exchange_symbol","")
	access_token = "access_token"
	booking_response = dict()
	aliceorderid=""

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
				data = form.cleaned_data
				print("serialize####---->", data)
				if data["transaction_type"]=="BUY":
					data["transaction_type"] = TransactionType.Buy
				else:
					data["transaction_type"] = TransactionType.Sell

				if data["ordertype"] == "MARKET":
					data["ordertype"]=OrderType.Market
				elif data["ordertype"] == "LIMIT":
					data["ordertype"]=OrderType.Limit
				elif data["ordertype"] == "SL":
					data["ordertype"]=OrderType.StopLossLimit
				else:
					data["ordertype"]=OrderType.StopLossMarket

				if data["product_type"]=="D":
					data["product_type"] = ProductType.Delivery
				elif data["product_type"]=="I":
					data["product_type"] = ProductType.Intraday
				elif data["product_type"]=="CO":
					data["product_type"] = ProductType.CoverOrder
				else:
					data["product_type"] = ProductType.BracketOrder



				if access_token in cache:
					alice_blue_order_place = alice_blue_object(cache.get(access_token))
					booking_response = alice_blue_order_place.place_order(transaction_type = data["transaction_type"],
                     instrument = alice_blue_order_place.get_instrument_by_symbol(data["exchange_name"], data["exchange_symbol"]),
                     quantity = data["quantity"],
                     order_type = data["ordertype"],
                     product_type = data["product_type"],
                     price = 0.0,
                     trigger_price = None,
                     stop_loss = None,
                     square_off = None,
                     trailing_sl = None,
                     is_amo = False)
					print(booking_response)
					if booking_response["status"] == "success":
						aliceorderid = booking_response["data"]["oms_order_id"]

				else:
					access_token_str = alice_blue_login()
					alice_blue_order_place = alice_blue_object(access_token_str)
					booking_response = alice_blue_order_place.place_order(transaction_type = data["transaction_type"],
                     instrument = alice_blue_order_place.get_instrument_by_symbol(data["exchange_name"], data["exchange_symbol"]),
                     quantity = data["quantity"],
                     order_type = data["ordertype"],
                     product_type = data["product_type"],
                     price = 0.0,
                     trigger_price = None,
                     stop_loss = None,
                     square_off = None,
                     trailing_sl = None,
                     is_amo = False)
					print(booking_response)
					if booking_response["status"] == "success":
						aliceorderid = booking_response["data"]["oms_order_id"]
					cache.set(access_token, access_token_str)
				
				PlaceOrder.objects.create(
					transaction_type=form.data["transaction_type"],
					alice_blue_order_id=aliceorderid,
					exchange_symbol=data["exchange_symbol"],
					input_symbol=data["input_symbol"],
					exchange_name=data["exchange_name"],
					instrumentname=data["instrumentname"],
					ordertype=form.data["ordertype"],
					quantity=data["quantity"],
					product_type=form.data["product_type"],
					max_profit=data["max_profit"],
					max_loss=data["max_loss"],
					strategy_tag=data["strategy_tag"]
					)

				return HttpResponse("success" + booking_response["data"]["oms_order_id"])
	return render(request,"index.html",{"form":form, "total_symbols_count": total_symbols_count})



def nse_index_quote(request):
	# if request.method=='POST':
	#   q = nse.get_quote(request.POST.get('symbol'))
	#   return JsonResponse(q, safe=False)
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
  json_data = open(str(settings.BASE_DIR) + '/main/stock_name_symbols.json')
  # json_data = open('stock_name_symbols.json')
  data1 = json.load(json_data)
  data2 = json.dumps(data1)
  NSE=StockExchange.objects.get(id=1)
  for key, value in data1.items():
      i = StockSymbolTable.objects.create(stock_name=value, stock_symbols=key)
      i.stock_exchange.add(NSE)
      print("completed")
  return JsonResponse("all data inserted", safe=False)

#example like this http://127.0.0.1:8001/tradingviewsignal/MRF/
def tradingviewsignal(request, pk):
	tradingviewdata = pk
	if tradingviewdata in cache:
		signal_data = cache.get(tradingviewdata)
		return JsonResponse(signal_data, safe=False)
	else:
		handler = TA_Handler(
				symbol=tradingviewdata,
				exchange="NSE",
				screener="india",
				interval=Interval.INTERVAL_1_MINUTE)
		analysis = handler.get_analysis()
		data = {
			"stock_symbols": analysis.symbol,
			"summary": analysis.summary,
			"oscillators": analysis.oscillators,
			"moving_averages": analysis.moving_averages,
			"time_created": analysis.time
			}
		cache.set(tradingviewdata, data, timeout=60*5)
		return JsonResponse(data, safe=False)

def signal_top_gainers(request):
	topgainers_signal = "topgainerssignal"
	if topgainers_signal in cache:
		signal_data = cache.get(topgainers_signal)
		return JsonResponse(signal_data, safe=False)
	else:
		top_gainer_nsetools = cache.get("topgainers")
		signal_data = []
		for i in top_gainer_nsetools:
			handler = TA_Handler(
					symbol=i,
					exchange="NSE",
					screener="india",
					interval=Interval.INTERVAL_1_MINUTE)
			analysis = handler.get_analysis()
			data = {
				"stock_symbols": analysis.symbol,
				"summary": analysis.summary,
				"oscillators": analysis.oscillators,
				"moving_averages": analysis.moving_averages,
				"time_created": analysis.time
				}
			signal_data.append(data)
	cache.set(topgainers_signal, signal_data, timeout=settings.CACHE_TIMEOUT)
	return JsonResponse(signal_data, safe=False)

def signal_top_losers(request):
	toplosers_signal = "toploserssignal"
	if toplosers_signal in cache:
		signal_data = cache.get(toplosers_signal)
		return JsonResponse(signal_data, safe=False)
	else:
		top_losers_nsetools = cache.get("toplosers")
		signal_data = []
		for i in top_losers_nsetools:
			handler = TA_Handler(
					symbol=i,
					exchange="NSE",
					screener="india",
					interval=Interval.INTERVAL_1_MINUTE)
			analysis = handler.get_analysis()
			data = {
				"stock_symbols": analysis.symbol,
				"summary": analysis.summary,
				"oscillators": analysis.oscillators,
				"moving_averages": analysis.moving_averages,
				"time_created": analysis.time
				}
			signal_data.append(data)
		cache.set(toplosers_signal, signal_data, timeout=settings.CACHE_TIMEOUT)
		return JsonResponse(signal_data, safe=False)


def top_gainers_list(request):
	topgainers = "topgainers"
	if topgainers in cache:
		top_gainers_data = cache.get(topgainers)
		return JsonResponse(top_gainers_data, safe=False)
	else:
		top_gainer_nsetools = requests.get(url="https://www1.nseindia.com/live_market/dynaContent/live_analysis/gainers/niftyGainers1.json").json()
		print(top_gainer_nsetools)
		# list_symbols = []
		# for i in top_gainer_nsetools:
		# 	list_symbols.append(i["symbol"])
		# cache.set(topgainers, list_symbols, timeout=settings.CACHE_TIMEOUT)
		return JsonResponse("null data", safe=False)

def top_losers_list(request):
	toplosers = "toplosers"
	if toplosers in cache:
		top_losers_data = cache.get(toplosers)
		return JsonResponse(top_losers_data, safe=False)
	else:
		top_loser_nsetools = requests.get(url="https://www1.nseindia.com/live_market/dynaContent/live_analysis/losers/niftyLosers1.json").json()
		print(top_loser_nsetools)
		list_symbols = []
		for i in top_loser_nsetools:
			list_symbols.append(i["symbol"])
		cache.set(toplosers, list_symbols, timeout=settings.CACHE_TIMEOUT)
		return JsonResponse(list_symbols, safe=False)

def nsetop50list(request):
	nse_fifty = "nse_fifty"
	if nse_fifty in cache:
		nse_fifty_list = cache.get(nse_fifty)
		return JsonResponse(nse_fifty_list, safe=False)
	else:
		nse_fifty_list = nse50bse30.getNSE50()["Tickers"]
		cache.set(nse_fifty, nse_fifty_list, timeout=3600*3)
		return JsonResponse(nse_fifty_list, safe=False)

def bsetop30list(request):
	bse_thirty = "bse_thirty"
	if bse_thirty in cache:
		bse_thirty_list = cache.get(bse_thirty)
		return JsonResponse(bse_thirty_list, safe=False)
	else:
		bse_thirty_list = nse50bse30.getBSE30()["Tickers"]
		cache.set(bse_thirty, bse_thirty_list, timeout=3600*3)
		return JsonResponse(bse_thirty_list, safe=False)


def signal_nse_50(request):
	nse_50 = "nse_50"
	if nse_50 in cache:
		signal_data = cache.get(nse_50)
		return JsonResponse(signal_data, safe=False)
	else:
		nse_50_list = cache.get("nse_fifty")
		signal_data = []
		for i in nse_50_list:
			handler = TA_Handler(
					symbol=i,
					exchange="NSE",
					screener="india",
					interval=Interval.INTERVAL_1_MINUTE)
			analysis = handler.get_analysis()
			data = {
				"stock_symbols": analysis.symbol,
				"summary": analysis.summary,
				"oscillators": analysis.oscillators,
				"moving_averages": analysis.moving_averages,
				"time_created": analysis.time
				}
			print(data)
			signal_data.append(data)
		cache.set(nse_50, signal_data, timeout=settings.CACHE_TIMEOUT)
		return JsonResponse(signal_data, safe=False)

def aliceblueordercancellation(request):
	access_token = "access_token"
	if request.method=="POST":
		order_id = request.POST["order_id"]
		if order_id:
			if access_token in cache:
				alice_blue = alice_blue_object(cache.get(access_token))
				cancel_order_response = alice_blue.cancel_order(order_id)
				return JsonResponse(cancel_order_response, safe=False)
			else:
				access_token = alice_blue_login()
				alice_blue = alice_blue_object(access_token)
				cancel_order_response = alice_blue.cancel_order(order_id)
				return JsonResponse(cancel_order_response, safe=False)
		else:
			return JsonResponse("Enter Order Id", safe=False)


def aliceblueorderhistory(request):
	access_token = "access_token"
	if request.method=="POST":
		order_id = request.POST["order_id"]
		if order_id:
			if access_token in cache:
				alice_blue = alice_blue_object(cache.get(access_token))
				order_history_response = alice_blue.get_order_history(order_id)
				return JsonResponse(order_history_response, safe=False)
			else:
				access_token = alice_blue_login()
				alice_blue = alice_blue_object(access_token)
				order_history_response = alice_blue.get_order_history(order_id)
				return JsonResponse(order_history_response, safe=False)
		else:
			return JsonResponse("Enter Order Id", safe=False)


def aliceblueallorderhistory(request):
	access_token = "access_token"
	if access_token in cache:
		alice_blue = alice_blue_object(cache.get(access_token))
		all_order_history_response = alice_blue.get_order_history()
		return JsonResponse(all_order_history_response, safe=False)
	else:
		access_token = alice_blue_login()
		alice_blue = alice_blue_object(access_token)
		all_order_history_response = alice_blue.get_order_history()
		return JsonResponse(all_order_history_response, safe=False)