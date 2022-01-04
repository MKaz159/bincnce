import math
import os
import pprint
from binance.client import Client
from datetime import datetime, timedelta
from dotenv import load_dotenv


# from tkinter import

load_dotenv()
API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')
client = Client(API_KEY, API_SECRET)
closing_time_index = 6
closing_price_index = 4


class Stock:
    def __init__(self, ticker, howlong):
        self.ticker = ticker
        self.howlong = howlong
        self.candle = []

    def GetHistoricalData(self):  # Retrieving the candle database
        """
        :param ticker:
        :param howLong:
        :return:
        list of list containing stock details (prices)
        """
        howLong = self.howlong
        # Calculate the timestamps for the binance api function
        untilThisDate = datetime.now()
        print(untilThisDate)
        sinceThisDate = untilThisDate - timedelta(days=howLong)
        print(sinceThisDate)
        # Execute the query from binance - timestamps must be converted to strings !
        try:
            candle = client.get_historical_klines(str(self.ticker), Client.KLINE_INTERVAL_1DAY, str(sinceThisDate),
                                                  str(untilThisDate))
            return candle
        except():
            print(f'unable to retrieve data for {self.ticker} ')
            return None


def GetMomentum(candle, time_index):  # Getting the DataBase and the week number
    closing_price = float(candle[time_index][closing_price_index])
    closing_price_weeklater = float(candle[time_index + 1][closing_price_index])
    momentum = closing_price - closing_price_weeklater
    time_stamp = candle[time_index + 1][closing_time_index]
    time_stamp = str((datetime.fromtimestamp(int(time_stamp / 1000))))
    time_stamp = time_stamp.split()
    return momentum, time_stamp[0]


def Get_axis_graph(candle):
    list_momentum = []
    list_closing_times = []
    i = 0
    for time_index in range(len(candle) - 1):
        momentum, close_time = GetMomentum(candle, i)
        list_momentum.append(math.floor(momentum))
        list_closing_times.append(close_time)
        i += 1
    x = list_closing_times
    y = list_momentum
    return x, y

def Get_axis_pricing_graph(candle):
    list_pricing = []
    list_closing_times = []
    for time_index in range(len(candle)):
        list_pricing.append(candle[time_index][closing_price_index])
        list_closing_times.append(candle[time_index][closing_time_index])
    x = list_closing_times
    y = list_pricing
    return x, y

def main():
    list_of_coins = []
    BTC = Stock('BTCUSDT', 30)
    BTC_candle = BTC.GetHistoricalData()
    ETH = Stock('ETHUSDT', 30)
    list_of_coins.append(BTC)

    BTC_x, BTC_y = Get_axis_graph(BTC_candle)
    print(f' The Time is {BTC_x[28]}')
    BTC_PRICE_x, BTC_PRICE_y = Get_axis_pricing_graph(BTC_candle)
    print(f' The Price is {BTC_y[28]}')

if __name__ == '__main__':
    main()
