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

    def GetHistoricalData(self):
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
        candle = client.get_historical_klines(str(self.ticker), Client.KLINE_INTERVAL_1WEEK, str(sinceThisDate),
                                              str(untilThisDate))
        return candle

    def GetMomentum(self,candle, week_number):
        closing_price = float(candle[week_number][closing_price_index])
        closing_price_weeklater = float(candle[week_number + 1][closing_price_index])
        momentum = closing_price - closing_price_weeklater
        time_stamp = candle[week_number + 1][closing_time_index]
        time_stamp = str((datetime.fromtimestamp(int(time_stamp / 1000))))
        time_stamp = time_stamp.split()
        return momentum, time_stamp[0]


def Get_axis_graph(CoinStock, candle):
    list_momentum = []
    list_closing_times = []
    i = 0
    for week in range(len(candle) - 1):
        momentum, close_time = CoinStock.GetMomentum(candle,i)
        list_momentum.append(momentum)
        list_closing_times.append(close_time)
        i += 1
    x = list_closing_times
    y = list_momentum
    return x, y


def main():
    BTC = Stock('BTCUSDT', 365)
    candle_db = BTC.GetHistoricalData()
    x, y = Get_axis_graph(BTC, candle_db)
    pprint.pprint(x)


if __name__ == '__main__':
    main()
