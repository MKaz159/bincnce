import binance
from binance.client import Client
from dotenv import load_dotenv
import os
import pprint
import sys
import math


load_dotenv()
API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')

if API_KEY is None or API_SECRET is None:
    sys.exit("Either `API_KEY` or `SECRET_KEY` env. variable is not defined!")
try:
    client = Client(API_KEY, API_SECRET)
except():
    print('Cant connect to api')
    sys.exit()

# Finding minimum values for everything
MKAZ_LIST = ['C','B','A']
asset = client.get_asset_balance(asset='BUSD')['free']
asset = float(asset)
print(asset)
asset_per_coin = asset/len(MKAZ_LIST)
print(asset_per_coin)
#precision = 8
#rounded_value = math.floor(asset * 10 ** precision) / 10**precision
#print(rounded_value)
#order = client.create_test_order(
#    symbol='ETHBUSD',
#    recvWindow=59000,
#    side=client.SIDE_BUY,
#    type=client.ORDER_TYPE_MARKET,
#    quoteOrderQty=rounded_value,
#)




