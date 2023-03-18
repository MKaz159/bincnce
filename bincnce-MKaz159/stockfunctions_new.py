import os
import time
import ast
import logging
from binance.client import Client
from binance.exceptions import *
from dotenv import load_dotenv
import concurrent.futures


load_dotenv()
client = Client(api_key=os.getenv('API_KEY'), api_secret=os.getenv('API_SECRET'))

default_list = ast.literal_eval(os.getenv('default_list'))
logging.basicConfig(filename='example.log', level=logging.INFO)


def timing_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"{func.__name__} elapsed time: {elapsed_time} seconds")
        return result
    return wrapper

class Stock:
    def __init__(self, symbol: str):
        self.symbol = symbol
        self.trading_ticker = symbol + 'BUSD'
        self.MKaz = client.get_historical_klines(symbol=self.trading_ticker, interval=Client.KLINE_INTERVAL_1DAY,start_str='10 days ago UTC')
        closing_price_today = float(self.MKaz[9][4])
        closing_price_10_days_sooner = float(self.MKaz[0][4])
        price_change = closing_price_today - closing_price_10_days_sooner
        self.momentum = price_change/closing_price_10_days_sooner * 100
        try:
            self.asset = client.get_asset_balance(asset=symbol)['free']
        except:
            self.asset = None
    @timing_decorator
    def Buyer(self, amount, test=False): # QA needed here to verify the amount is OK.
        logging.debug(f'Buyer function initiated for {self.symbol}')
        '''
        :param amount: Amount is an integer representing the amount of money to buy with
        :return: API response from the server
        '''
        if not test:
            try:
                 order = client.order_market_buy(
                    symbol=self.trading_ticker,
                    recvWindow=59000,
                    quoteOrderQty=amount)
                 logging.info(f'Purchased {amount} of {self.symbol}.')
                 return order
            except BinanceOrderMinAmountException:
                logging.error(f'failed to place a purchase for {self.trading_ticker} due to minimum amount.'
                      f' Check parameter inserted to the function')
                return None
        else:
            try:
                order = client.create_test_order(
                    symbol=self.trading_ticker,
                    recvWindow=59000,
                    side=client.SIDE_BUY,
                    type=client.ORDER_TYPE_MARKET,
                    quoteOrderQty=amount,
                )
                return order
            except BinanceOrderMinAmountException:
                logging.error(f'failed to place a purchase for {self.trading_ticker} due to minimum amount.'
                      f' Check parameter inserted to the function')
                return None

    @timing_decorator
    def Seller(self, amount, test=False):
        logging.debug(f'Seller function initiated for {self.symbol}')
        if not test:
            try:
                order = client.order_market_sell(recvWindow=59000,
                    symbol=self.trading_ticker,
                    quantity=amount,
                )
                logging.info(f'Sold {amount} of {self.symbol}')
                return order
            except BinanceOrderMinAmountException:
                logging.error(f'failed to place a selling for {self.trading_ticker} due to minimum amount.'
                      f' Check parameter inserted to the function')
        else:
            try:
                order = client.create_test_order(
                    symbol=self.trading_ticker,
                    recvWindow=59000,
                    side=client.SIDE_SELL,
                    type=client.ORDER_TYPE_MARKET,
                    quantity=amount,
                )
                logging.info(f'Sold {amount} of {self.symbol}')
                return order
            except BinanceOrderMinAmountException:
                logging.error(f'failed to place a selling for {self.trading_ticker} due to minimum amount.'
                      f' Check parameter inserted to the function')

@timing_decorator
def Dictionary_stocks(default_list):
    stonks_list = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(Stock, ticker) for ticker in default_list]
        for future in concurrent.futures.as_completed(futures):
            stonks_list.append(future.result())
    sorted_stonks_by_momentum = sorted(stonks_list, key=lambda s: s.momentum, reverse=True)
    return sorted_stonks_by_momentum








if __name__ == '__main__':
    Dictionary_stocks(default_list)

