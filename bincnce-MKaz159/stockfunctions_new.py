import os
import time
import ast
import logging
from binance.client import Client
from binance.exceptions import *
from dotenv import load_dotenv
import concurrent.futures
from typing import List, Dict
import math

load_dotenv()
client = Client(api_key=os.getenv('API_KEY'), api_secret=os.getenv('API_SECRET'))

default_list = ast.literal_eval(os.getenv('default_list'))
logging.basicConfig(filename='example.log', filemode='w', level=logging.INFO,
                    format='%(asctime)s-%(levelname)s- %(message)s ', datefmt='%m/%d/%Y %I:%M:%S')



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
        min_notional = 0.0

        self.symbol = symbol
        self.trading_ticker = symbol + 'BUSD'
        MKaz = client.get_historical_klines(symbol=self.trading_ticker, interval=Client.KLINE_INTERVAL_1DAY,
                                            start_str='10 days ago UTC')
        closing_price_today = float(MKaz[9][4])
        closing_price_10_days_sooner = float(MKaz[0][4])
        price_change = closing_price_today - closing_price_10_days_sooner
        self.momentum = price_change / closing_price_10_days_sooner * 100
        try:
            asset = client.get_asset_balance(asset=symbol)['free']
            self.asset = float(asset)
        except:
            self.asset = None

        # Can i even sell this coin ?

    @timing_decorator
    def Buyer(self, amount, test=True):  # QA needed here to verify the amount is OK.
        logging.info(f'Buyer function initiated for {self.symbol}')
        '''
        :param amount: Amount is an integer representing the amount of money to buy with
        :return: API response from the server
        '''
        if not test:
            try:
                client.order_market_buy(
                    symbol=self.trading_ticker,
                    recvWindow=59000,
                    quoteOrderQty=amount)
                logging.info(f'Purchased {amount} of {self.symbol}.')
            except BinanceOrderMinAmountException:
                logging.error(f'failed to place a purchase for {self.trading_ticker} due to minimum amount.'
                              f' Check parameter inserted to the function')
        else:
            try:
                client.create_test_order(
                    symbol=self.trading_ticker,
                    recvWindow=59000,
                    side=client.SIDE_BUY,
                    type=client.ORDER_TYPE_MARKET,
                    quoteOrderQty=amount,
                )
            except BinanceAPIException as Expect:
                logging.error(f'failed to place a buying for {self.trading_ticker} due to {Expect}.')

    @timing_decorator
    def Seller(self, test=True):
        logging.info(f'Seller function initiated for {self.symbol}')

        if not test:
            try:
                print(f'mayday mayday real buy order initated ')
                order = client.order_market_sell(recvWindow=59000,
                                                 symbol=self.trading_ticker,
                                                 quantity=self.asset,
                                                 )
                logging.info(f'Sold {self.asset} of {self.symbol}')
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
                    quantity=self.asset,
                )
                logging.info(f'Sold {self.asset} of {self.symbol}')
                return order
            except BinanceAPIException as Expect:
                logging.error(f'failed to place a selling for {self.trading_ticker} due to {Expect}.')


@timing_decorator
def Sorted_stonks_dict(default_list):
    '''
    :param default_list: [''BTC','ETH','XRP'] on so on
    :return: [Stock(BTC),] and so on based on momentum values
    '''
    stonks_list = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(Stock, ticker) for ticker in default_list]
        for future in concurrent.futures.as_completed(futures):
            stonks_list.append(future.result())
    sorted_stonks_by_momentum = sorted(stonks_list, key=lambda s: s.momentum, reverse=True)
    stock_dict = {stock.symbol: stock for stock in sorted_stonks_by_momentum}
    logging.info(f'sorted stock dict created.')
    return stock_dict


def Who_to_buy(momentum_sorted_stock_instances: List[Stock]):
    wallet_goal = []
    for iteration_number in range(0, 3):
        if momentum_sorted_stock_instances[iteration_number].momentum > 0:
            wallet_goal.append(momentum_sorted_stock_instances[iteration_number].symbol)
    logging.info(f'The destination of coins is = {wallet_goal}')
    return wallet_goal


@timing_decorator
def Who_To_sell(momentum_sorted_stock_instances: List[Stock]):
    '''
    The function is able to return the sellable assets the client holds
    :return:
    list of objects to be sold
    '''
    to_be_sold = []
    dict_of_stock = {}
    all_account_assets = client.get_account()
    non_zero_balance = [coin_name['asset'] for coin_name in all_account_assets['balances']
                        if float(coin_name['free']) + float(coin_name['locked'])]

    # owned_asset_filtered are the owned assets that have an instanciation of class Stock()
    owned_asset_filtered = [coin for coin in non_zero_balance if coin in default_list]

    wallet_goal = Who_to_buy(momentum_sorted_stock_instances)

    for symbol_owned_asset in owned_asset_filtered:
        if symbol_owned_asset not in wallet_goal:
            to_be_sold.append(symbol_owned_asset)

    logging.info(f'User owns {owned_asset_filtered} with targeted {wallet_goal}. Decided to sell {to_be_sold}')
    return to_be_sold, owned_asset_filtered


def Selling_outdated_stock(stock_dict: Dict[str, Stock], list_for_selling):
    for coin_to_sell in list_for_selling:
        seller_candidate = stock_dict.get(coin_to_sell)
        try:
            seller_candidate.Seller(test=False)
        except BinanceAPIException as execpt:
            print(f' Failed to initiate sell on {seller_candidate.symbol} with the {execpt}')
def Buyer_new_destination(stock_dict: Dict[str, Stock], buy_target):
    precision = 8
    BUSD_balance =client.get_asset_balance(asset='BUSD')['free']
    logging.info(f'Buyer initiated with {BUSD_balance}')
    BUSD_balance = float(BUSD_balance)
    BUSD_balance_per_coin = BUSD_balance/len(buy_target)
    logging.info(f'Total BUSD is {BUSD_balance} while having {len(buy_target)} coins. {BUSD_balance_per_coin}$')
    BUSD_rounded = math.floor(BUSD_balance_per_coin * 10 ** precision) / 10**precision
    logging.info(f'Preparing to buy individual stocks. Per coin {BUSD_rounded}')
    for coin_to_buy in buy_target:
        buy_candidate = stock_dict.get(coin_to_buy)
        buy_candidate.Buyer(amount=BUSD_rounded,test=False)

def Convert_Dust_assets(stock_dict: Dict[str, Stock], buy_target):
    pass

if __name__ == '__main__':
    stock_dict = Sorted_stonks_dict(default_list)  # A list of stock instances sorted by momentum
    list_of_destined_to_sell, filtered_owned_assets = Who_To_sell(list(stock_dict.values()))  # A list of symbols
    buy_target = Who_to_buy(list(stock_dict.values()))
    Selling_outdated_stock(stock_dict, list_of_destined_to_sell)
    time.sleep(30)
    Buyer_new_destination(stock_dict, buy_target)
