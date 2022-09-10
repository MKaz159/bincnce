import binance
from binance.client import Client
from dotenv import load_dotenv
import os
import pprint
import sys
import math

amount = 0.485
total = (amount - 0.001) % 0.001
print(total)
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



def round_down(coin, number):
    info = client.get_symbol_info(coin)
    step_size = [float(_['stepSize']) for _ in info['filters'] if _['filterType'] == 'LOT_SIZE'][0]
    step_size = '%.8f' % step_size
    step_size = step_size.rstrip('0')
    decimals = len(step_size.split('.')[1])
    return math.floor(number * 10 ** decimals) / 10 ** decimals

quantity = round_down('BNBBUSD', 0.485)
print(quantity)
client.create_test_order(recvWindow=59000,
                         symbol='BNBBUSD',
                         side=Client.SIDE_SELL,
                         type=Client.ORDER_TYPE_MARKET,
                         quantity=quantity)


