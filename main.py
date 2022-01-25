import math
import os
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
        else:
            self.howlong = howlong
        untilThisDate = datetime.now()
        sinceThisDate = untilThisDate - timedelta(days=self.howlong)
        try:
            self.candle = client.get_historical_klines(str(self.ticker), Client.KLINE_INTERVAL_1DAY, str(sinceThisDate),
                                                       str(untilThisDate))
        except:
            print(f'unable to retrieve data for {self.ticker} ')
            self.candle = []

    # Returns Certains dates
    def Get_axis_pricing_graph(self):
        list_pricing = []
        list_closing_times = []
        for time_index in range(len(self.candle)):
            list_pricing.append(float(self.candle[time_index][closing_price_index]))
            list_closing_times.append(self.candle[time_index][closing_time_index])
        x = list_closing_times
        y = list_pricing
        return x, y

    # Get's you momentum and time stamp for a certain position in the candle database
    def GetMomentum(self, time_index) -> object:
        """
        :param candle:
        :param time_index:
        :return:
        The Momentum Value and the day for which it was calculated
        """
        if not self.candle:
            return 0, 0
        closing_price = float(self.candle[time_index][closing_price_index])
        closing_price_10days_earlier = float(self.candle[time_index - 10][closing_price_index])
        momentum = closing_price - closing_price_10days_earlier
        time_stamp = self.candle[time_index][closing_time_index]
        time_stamp = str((datetime.fromtimestamp(int(time_stamp / 1000))))
        time_stamp = time_stamp.split()
        return momentum.__round__(), time_stamp[0]

    # Calculates the momentum values over time
    def Get_axis_graph(self):
        """
        :param candle:
        :return:
        The X and Y axis for the selected candle DB (per stock)
        """
        list_momentum = []
        list_closing_times = []
        for i in range(10, len(self.candle)):
            momentum, close_time = self.GetMomentum(i)
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
    raw_coin_list = []
    coin_list = []
    usr_input = ''
    while usr_input != 'stop':
        usr_input = input('Enter Your coin pairs ("stop" in order to exit) : ')
        raw_coin_list.append((usr_input.upper()))
    raw_coin_list.pop()
    # if coin list is empty we use default list which is likely better than your list
    if not raw_coin_list:
        raw_coin_list = ast.literal_eval(os.getenv('default_list'))
        for coin in raw_coin_list:
            coin_list.append(Stock(coin))
    else:
        for coin in raw_coin_list:
            if Stock(coin).candle:
                coin_list.append(Stock(coin))
            else:
                print(f'coin {coin} aint getting in ')
    for coin in coin_list:
        try:
            coin_to_candle_DB.update({coin.ticker: coin})
        except():
            print(f'{coin.ticker} is not a coin')
    return coin_to_candle_DB  # for example {'BNBBUSD': Stock('BNBBUSD')


def Get_buy_appraisal(coin_to_candle_dictionary):
    """
    :param coin_to_candle_dictionary:
    :return:
    Who are the Three stocks who got the highest momentum today
    """
    for key, value in coin_to_candle_dictionary.items():
        momentum_value, momentum_time = value.GetMomentum(len(value.candle) - 1)
        stocks_momentum.update({key: momentum_value})
    highest_keys = sorted(stocks_momentum, key=stocks_momentum.get, reverse=True)[:3]
    for i in highest_keys:
        print(f'Buy {i}')


def main():
    coin_database = GetValues()
    Get_buy_appraisal(coin_database)
    # Assume that i want the value for BNB and BNB is inside of my list
    x, y = Stock.Get_axis_graph(coin_database['XRPBUSD'])
    XRP_PRICE_x, XRP_PRICE_y = Stock.Get_axis_pricing_graph(coin_database['XRPBUSD'])
    print (XRP_PRICE_y[59])


if __name__ == '__main__':
    main()
