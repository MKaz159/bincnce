from stockfunctions import *


def GetOwnedAssets():
    """
    :return:
    {'BTC': 1, 'ETH':2}
    """
    new_dict = {}
    balances = client.get_account()['balances']
    for asset_dictionary in balances:
        # now you have i = {'asset': 'BTC', 'free': '0.00001666', 'locked': '0.00000000'}
        if float(asset_dictionary['free']) > 0:
            new_dict.update({asset_dictionary['asset']: asset_dictionary['free']})
    return new_dict


def Compare_Between_owned(owned_stocks, stocks_desired):
    """
    :param owned_stocks: [BTC,
    :param stocks_desired:
    :return:
    A list of stocks that are going to be bought (AKA not in owned_stocks but are in desired
    """
    what_should_i_buy = []
    sorted_desired_stocks = []
    for x in stocks_desired:
        sorted_desired_stocks.append(x.replace('BUSD', ''))
    for stock in sorted_desired_stocks:
        if stock not in owned_stocks:
            what_should_i_buy.append(stock + 'BUSD')

    return what_should_i_buy


# When the calculation occurs
def coin_to_coinBUSD(owned_coins):
    coin_with_BUSD = []
    BUSD_with_coin = owned_coins.keys()
    for coin in BUSD_with_coin:
        coin_with_BUSD.append(coin + 'BUSD')
    return coin_with_BUSD


def main():
    TOTAL_BALANCE = 0
    coin_database = GetValues()  # for example {'BNBBUSD': Stock('BNBBUSD')
    desired_coins = Get_buy_appraisal(coin_database)  # for example ['BNBBUSD','ATOMBUSD','ETHBUSD']
    owned_coins = GetOwnedAssets()  # for example {'BNB': 0.01, 'ETH':3}
    buyer = Compare_Between_owned(owned_coins, desired_coins)  # ['BNBBUSD', 'ADABUSD']
    owned_coin_pairs = coin_to_coinBUSD(owned_coins)
    for selling_coin in owned_coin_pairs:
        if selling_coin in desired_coins:  # if a coin is desired and and is owned
            print(f"Your coin {selling_coin} hasn't been sold")
        elif selling_coin != 'BUSDBUSD':  # if a coin desired and not owned
            try:
                coin_database[selling_coin].Sellers_remorse()
                print(f'SOLD {selling_coin} for 30$ ')
                TOTAL_BALANCE += 30
            except:
                print(f"Couldn't sell {selling_coin} it isn't listed on the market")
    for buying_coin in buyer:
        coin_database[buying_coin].Buyers_regret()
        print(f'BOUGHT {buying_coin} for 30$')
        TOTAL_BALANCE -= 30
    print(TOTAL_BALANCE)


if __name__ == '__main__':
    main()
