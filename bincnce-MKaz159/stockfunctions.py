import math
import os
import ast
from binance.client import Client
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Default parameters
closing_time_index = 6
closing_price_index = 4
coin_to_candle_DB = {}
stocks_momentum = {}

# All the default values that will be used in this program
load_dotenv()
API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')

# Connecting the API
client = Client(API_KEY, API_SECRET)


# Class containing ticker info and candle history for 20 days (Daily Candle)
class Stock:
    def __init__(self, ticker):
        self.ticker = ticker
        untilThisDate = datetime.now()
        sinceThisDate = untilThisDate - timedelta(days=20)

        self.candle = client.get_historical_klines(str(self.ticker), Client.KLINE_INTERVAL_1DAY, str(sinceThisDate),
                                                   str(untilThisDate))
    def __str__(self):
        print(f'')
    def round_down(self, number):
        info = client.get_symbol_info(self.ticker)
        step_size = [float(_['stepSize']) for _ in info['filters'] if _['filterType'] == 'LOT_SIZE'][0]
        step_size = '%.8f' % step_size
        step_size = step_size.rstrip('0')
        decimals = len(step_size.split('.')[1])
        return math.floor(float(number) * 10 ** decimals) / 10 ** decimals

    # What is the minimum price for a ticker Used in the BUY SIDE
    def get_minimum_price(self):
        value = ''
        filters = client.get_symbol_info(self.ticker)["filters"]
        for i in filters:
            if i["filterType"] == "MIN_NOTIONAL":
                value = i['minNotional']
        return value

    # What is the minimum quantity for a ticker Used in the SELL side
    def get_minimum_quantity(self):
        print(f'fetching price for {self.ticker}')
        filters = client.get_symbol_info(self.ticker)["filters"]
        for i in filters:
            if i["filterType"] == "LOT_SIZE":
                value = i['minQty']
        return value

    # Buying a coin with a X amount of BUSD with inspection of minimum pricing.

    def Buyers_regret(self, amount):
        """
        :param amount:
        :return: Purchase done with {amount} of $
        """
        amount_new = self.round_down(amount)
        if amount > float(self.get_minimum_price()):
            client.create_test_order(recvWindow=59000,
                symbol=str(self.ticker),
                side=Client.SIDE_SELL,
                type=Client.ORDER_TYPE_MARKET,
                quoteOrderQty=amount_new)
            tmp_str = f'Bought {self.ticker} {amount_new}$ \n'
            return tmp_str
        else:
            tmp_str = f'Couldnt buy {self.ticker}, {amount_new}$ is to little'
            return tmp_str

    def Sellers_remorse(self, amount):
        '''
        :param amount:
        :return: Selling amount of coin
        '''
        amount_new = self.round_down(amount)
        min_QTY = float(self.get_minimum_quantity())
        if float(amount_new) > float(min_QTY):
            print(f'passed inspection sale intiated for {amount_new} on BNB ')
            client.create_test_order(recvWindow=59000,
                symbol=str(self.ticker),
                side=Client.SIDE_SELL,
                type=Client.ORDER_TYPE_MARKET,
                quantity=amount_new)
            tmp_str = f'SOLD {self.ticker} {amount_new} units\n'
            return tmp_str
        else:
            tmp_str = f'Couldnt sell {self.ticker}, {amount_new}$ is to little\n'
            return tmp_str

    # Get's you momentum and time stamp for a certain position in the candle database
    def GetMomentum(self) -> object:
        """
        :param time_index:
        :return:
        The Momentum Value and the day for which it was calculated
        """
        closing_price = float(self.candle[0][closing_price_index])
        closing_price_10days_earlier = float(self.candle[0 - 10][closing_price_index])
        momentum = closing_price - closing_price_10days_earlier
        time_stamp = self.candle[0][closing_time_index]
        time_stamp = str((datetime.fromtimestamp(int(time_stamp / 1000))))
        time_stamp = time_stamp.split()
        return momentum, time_stamp[0]


def GetValues():
    """
    :return:
    TEMPORARY FUNCTION
    """
    coin_to_candle_DB = {}
    # i.e ['BNBBUSD','ETHBUSD]
    default_list = ast.literal_eval(os.getenv('default_list'))
    for coin_pair in default_list:
        coin_to_candle_DB.update({coin_pair: Stock(coin_pair)})
    return coin_to_candle_DB  # for example {'BNBBUSD': Stock('BNBBUSD')


def Get_buy_appraisal(coin_to_candle_dictionary):
    top3_stock_lst = []
    """
    :param coin_to_candle_dictionary:
    :return:
    Who are the Three stocks who got the highest momentum today
    """
    for key, value in coin_to_candle_dictionary.items():
        momentum_value, momentum_time = value.GetMomentum(len(value.candle) - 1)
        if momentum_value > 0:
            stocks_momentum.update({key: momentum_value})
    # pprint(stocks_momentum)
    highest_keys = sorted(stocks_momentum, key=stocks_momentum.get, reverse=True)[:3]
    for i in highest_keys:
        top3_stock_lst.append(i)
    return top3_stock_lst


def main():
    BNB = Stock('BNBBUSD')
    momentum,timestamp = BNB.GetMomentum()
    print(f'The momentum is {momentum}, While timestamp is {timestamp}')




if __name__ == '__main__':
    main()
