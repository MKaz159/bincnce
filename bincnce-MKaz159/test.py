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
info = client.get_symbol_info('SOLBUSD')

filters = info['filters']
for filter in filters:
    if filter['filterType'] == 'LOT_SIZE':
        print(filter['stepSize'])


def modify_value_cancer(number, step_size):
    if step_size == 1.0:
        modified_value = math.floor(number)
    else:
        remainder = number % step_size
        if remainder == 0:
            modified_value = number
        elif remainder > 0.5 * step_size:
            modified_value = math.ceil(number / step_size) * step_size
        else:
            modified_value = math.floor(number / step_size) * step_size
    return modified_value



def modify_value(number, step_size):
    if step_size == 1.0:
        modified_value = math.floor(number)
    else:
        modified_value = round(number - (number % step_size), int(-math.log10(step_size)))
    return modified_value



mkaz_value = modify_value(6.63, 0.01000000)

print(mkaz_value)
print(George)
#symbol_info = exchange_info['symbols']
#for symbol in symbol_info:
#    if symbol['symbol'] == 'SHIBBUSD':
#        print(symbol['filters'])
#
#order = client.create_test_order(
#    symbol='BNBBUSD',
#    recvWindow=59000,
#    side=client.SIDE_SELL,
#    type=client.ORDER_TYPE_MARKET,
#    quantity=0.434001,
#)
#
#order = client.order_market_sell(recvWindow=59000,
#                                 symbol='BNBBUSD',
#                                 quantity=0.020001,
#                                 )


