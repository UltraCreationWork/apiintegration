from django.shortcuts import render
from django.contrib.auth.models import User
import random
from MetaTrader5 import *
import requests
from django.http import JsonResponse
import json
import pandas as pd
initialize(               
		login=33003,              
		password="pdge2iej",     
		server="Sharon-Live",                   
		portable=False         
	)
symbols_total=symbols_total()
exchange_list=['USD','NSE', 'BSE', 'FOREX']

def get_symbols(request):
	data=dict()
	for i in exchange_list:
		symbols = symbols_get(group=i)
		data[i]=symbols
	maindata = pd.Series(data)
	# print(maindata)
	print(data)
	data=json.dumps(symbols)
	print(data)
	return JsonResponse(data,safe=False)



def home(request):
	return render(request,"index.html",{"symbols":symbols_total})



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




