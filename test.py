import pandas as pd
from binance.client import Client
from main import *
import os
from dotenv import load_dotenv
import time
from binance.client import Client
from datetime import datetime

load_dotenv()
coin_list = []
API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')
client = Client(API_KEY, API_SECRET)
coin_to_candle_DB = {}
stocks_momentum = {}

def GetValues():
    usr_input = ''
    while usr_input != 'stop':
        usr_input = input('Enter Your coin pairs ("stop" in order to exit) : ')
        coin_list.append(Stock(usr_input))
    coin_list.pop()
    return coin_list


for coin in GetValues():
    coin_to_candle_DB.update({coin.ticker: coin.GetHistoricalData})
for key, value in coin_to_candle_DB.items():
    print(key)
    stocks_momentum
# def Printing_Best_momentum(coins):
