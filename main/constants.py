from alice_blue import *

USERNAME="196682"
PASSWORD="Om@123456"
TWOFA="1"
APPSECRET="26yq2cyJqSzDwkPhEnGXsTaNUDXrFheQcAdnju87cjaQa89YQDxduFBDjNUtNhTK"
APPID="TdOmJDaL1z"
exchanges = ['NSE', 'BSE', 'BFO', 'NSE', 'NFO', 'MCX', 'CDS', 'NFO', 'CDS', 'CDS']

def alice_blue_login():
	return AliceBlue.login_and_get_access_token(username=USERNAME,
		password=PASSWORD,
		twoFA='1',
		 api_secret=APPSECRET,
		 app_id=APPID
		 )

def alice_blue_object(access_token: str):
	return AliceBlue(username=USERNAME,
		password=PASSWORD,
		access_token=access_token,
		master_contracts_to_download=['NSE', 'BSE']
		)

form_respnse = {
	'transaction_type': 'BUY',
	'exchange_symbol': 'REPL',
	'input_symbol': 'REPL#',
	'exchange_name': 'NSE',
	'instrumentname': 'EQ',
	'ordertype': 'MARKET',
	'quantity': 1,
	'product_type': 'D',
	'max_profit': 1.0,
	'max_loss': 1.0,
	'strategy_tag': 'START1'
	}