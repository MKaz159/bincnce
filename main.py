import math
import os
import pprint
import ast
from binance.client import Client
from datetime import datetime, timedelta
from dotenv import load_dotenv

# All the default values that will be used in this program
load_dotenv()
API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')
client = Client(API_KEY, API_SECRET)
closing_time_index = 6
closing_price_index = 4
coin_to_candle_DB = {}
stocks_momentum = {}


# Class containing ticker info and candle history for 60 days (Daily Candle)
class Stock:
    def __init__(self, ticker, howlong=None):
        self.ticker = ticker
        if howlong is None:
            self.howlong = 60
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
        sinceThisDate = untilThisDate - timedelta(days=howLong)
        # Execute the query from binance - timestamps must be converted to strings !
        try:
            candle = client.get_historical_klines(str(self.ticker), Client.KLINE_INTERVAL_1DAY, str(sinceThisDate),
                                                  str(untilThisDate))
            return candle
        except():
            print(f'unable to retrieve data for {self.ticker} ')
            pass


# Returns Certains dates
def Get_axis_pricing_graph(candle):
    list_pricing = []
    list_closing_times = []
    for time_index in range(len(candle)):
        list_pricing.append(float(candle[time_index][closing_price_index]))
        list_closing_times.append(candle[time_index][closing_time_index])
    x = list_closing_times
    y = list_pricing
    return x, y


# Get's you momentum and time stamp for a certain position in the candle database
def GetMomentum(candle, time_index):
    """
    :param candle:
    :param time_index:
    :return:
    The Momentum Value and the day for which it was calculated
    """
    closing_price = float(candle[time_index][closing_price_index])
    closing_price_10days_earlier = float(candle[time_index - 10][closing_price_index])
    momentum = closing_price - closing_price_10days_earlier
    time_stamp = candle[time_index][closing_time_index]
    time_stamp = str((datetime.fromtimestamp(int(time_stamp / 1000))))
    time_stamp = time_stamp.split()
    return momentum.__round__(), time_stamp[0]


# Calculates the momentum values over time
def Get_axis_graph(candle):
    """
    :param candle:
    :return:
    The X and Y axis for the selected candle DB (per stock)
    """
    list_momentum = []
    list_closing_times = []
    for i in range(10, len(candle)):
        momentum, close_time = GetMomentum(candle, i)
        list_momentum.append(math.floor(momentum))
        list_closing_times.append(close_time)
    x = list_closing_times
    y = list_momentum
    return x, y


# Will be replaced by checklist in tkinter
def GetValues():
    """
    :return:
    TEMPORARY FUNCTION
    """
    coin_list = []
    usr_input = ''
    while usr_input != 'stop':
        usr_input = input('Enter Your coin pairs ("stop" in order to exit) : ')
        coin_list.append(Stock(usr_input.upper()))
    coin_list.pop()
    # if coin list is empty we use default list which is likely better than your list
    if not coin_list:
        raw_coin_list = ast.literal_eval(os.getenv('default_list'))
        for coin in raw_coin_list:
            coin_list.append(Stock(coin))
    for coin in coin_list:
        try:
            coin_to_candle_DB.update({coin.ticker: coin.GetHistoricalData()})
        except:
            print(f'{coin.ticker} is not a coin')
    return coin_to_candle_DB


def Get_buy_appraisal(coin_to_candle_dictionary):
    """
    :param coin_to_candle_dictionary:
    :return:
    Who are the Three stocks who got the highest momentum today
    """
    for key, value in coin_to_candle_dictionary.items():
        momentum_value, momentum_time = GetMomentum(value, len(value) - 1)
        stocks_momentum.update({key: momentum_value})
    highest_keys = sorted(stocks_momentum, key=stocks_momentum.get, reverse=True)[:3]
    for i in highest_keys:
        print(f'Buy {i}')


def main():
    coin_database = GetValues()
    Get_buy_appraisal(coin_database)
    # Assume that i want the value for BNB and BNB is inside of my list
    x, y = Get_axis_graph(coin_database['BNBBUSD'])
    BTC_PRICE_x, BTC_PRICE_y = Get_axis_pricing_graph(coin_database['BNBBUSD'])


if __name__ == '__main__':
    main()
