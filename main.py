import os
import pprint
from config import api_key, api_secret, closing_price_index, closing_time_index
from binance.client import Client
from datetime import datetime, timedelta

client = Client(api_key, api_secret)


def GetHistoricalData(howLong, ticker):
    """
    :param ticker:
    :param howLong:
    :return:
    list of list containing stock details (prices)
    """
    howLong = howLong
    # Calculate the timestamps for the binance api function
    untilThisDate = datetime.now()
    print(untilThisDate)
    sinceThisDate = untilThisDate - timedelta(days=howLong)
    print(sinceThisDate)
    # Execute the query from binance - timestamps must be converted to strings !
    candle = client.get_historical_klines(str(ticker), Client.KLINE_INTERVAL_1WEEK, str(sinceThisDate),
                                          str(untilThisDate))
    return candle


def GetMomentum(candle_data, i):
    """
    :param candle_data:
    :param i:
    :return:
    Momentum Value & Closing TimeStamp
    """
    closing_price = float(candle_data[i][closing_price_index])
    closing_price_weeklater = float(candle_data[i + 1][closing_price_index])
    momentum = closing_price - closing_price_weeklater
    time_stamp = candle_data[i + 1][closing_time_index]
    time_stamp = str((datetime.fromtimestamp(int(time_stamp / 1000))))
    time_stamp = time_stamp.split()
    return momentum, time_stamp[0]


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
