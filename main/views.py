from django.shortcuts import render
from django.contrib.auth.models import User
import random
from MetaTrader5 import *
import requests
from django.http import JsonResponse
import json
import pandas as pd
from nsetools import Nse

# initialize(               
# 		login=33003,              
# 		password="pdge2iej",     
# 		server="Sharon-Live",                   
# 		portable=False         
# # 	)
# symbols_total=symbols_total()
# exchange_list=['USD','NSE', 'BSE', 'FOREX']


# def get_symbols(request):
# 	data=dict()
# 	for i in exchange_list:
# 		symbols = symbols_get(group=i)
# 		data[i]=symbols
# 	maindata = pd.Series(data)
# 	# print(maindata)
# 	print(data)
# 	data=json.dumps(symbols)
# 	print(data)
# 	return JsonResponse(data,safe=False)

nse = Nse()

def home(request):
	return render(request,"index.html",{"symbols": 500})

def symbols(request):
	all_stock_codes = nse.get_stock_codes()
	return JsonResponse(all_stock_codes,safe=False)

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




