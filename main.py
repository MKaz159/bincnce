import os
import pprint
from binance.client import Client
from datetime import datetime, timedelta
from dotenv import load_dotenv

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

    def get_axis_for_ohclv(self):
        list_momentum = []
        list_closing_times = []
        howLong = self.howlong
        ticker = self.ticker
        # Calculate the timestamps for the binance api function
        untilThisDate = datetime.now()
        print(untilThisDate)
        sinceThisDate = untilThisDate - timedelta(days=howLong)
        print(sinceThisDate)
        # Execute the query from binance - timestamps must be converted to strings !
        candle = client.get_historical_klines(str(ticker), Client.KLINE_INTERVAL_1WEEK, str(sinceThisDate),
                                              str(untilThisDate))
        i = 0
        closing_price = float([i][closing_price_index])
        closing_price_weeklater = float([i + 1][closing_price_index])
        momentum = closing_price - closing_price_weeklater
        time_stamp = [i + 1][closing_time_index]
        time_stamp = str((datetime.fromtimestamp(int(time_stamp / 1000))))
        time_stamp = time_stamp.split()
        date = time_stamp[0]
        for length_of_weeks in range(len(candle) - 1):


def GetStockPricing(candle_data):
    """
    :return:
    A list containing stock closing prices in weekly candles
    throughout the year
    """
    stock_prices = []
    for week in candle_data:
        stock_prices.append(week[closing_price_index])
    return stock_prices


def Get_axis_graph(candle_data):
    list_momentum = []
    list_closing_times = []
    i = 0
    for length_of_weeks in range(len(candle_data) - 1):
        momentum, close_time = GetMomentum(candle_data, i)
        list_momentum.append(momentum)
        list_closing_times.append(close_time)
        i += 1
    x = list_momentum
    y = list_closing_times
    return x, y


def main():
    ticker = 'BTCUSDT'
    candle_data = GetHistoricalData(365, ticker)
    x, y = Get_axis_graph(candle_data)
    stock_prices = GetStockPricing(candle_data)


if __name__ == '__main__':
    main()
