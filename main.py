from stockfunctions import *


def get_minimum_price(ticker):
    filters = client.get_symbol_info(ticker)["filters"]
    for i in filters:
        if i["filterType"] == "PRICE_FILTER":
            value = i['minPrice']
            print(f"the minimum price for {ticker} is {i['minPrice']}")
    return value


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
    print(f' The desired coins are {desired_coins} \n')
    owned_coins = GetOwnedAssets()  # for example {'BNB': 0.01, 'ETH':3}
    buyer = Compare_Between_owned(owned_coins, desired_coins)  # ['BNBBUSD', 'ADABUSD']
    owned_coin_pairs = coin_to_coinBUSD(owned_coins)
    for selling_coin in owned_coin_pairs:
        if selling_coin in desired_coins:  # if a coin is desired and and is owned
            print(f"Your coin {selling_coin} hasn't been sold cause it is in the desired coins\n")
        elif selling_coin != 'BUSDBUSD':  # if a coin desired and not owned
            try:
                amount_of_coin = owned_coins[selling_coin.replace('BUSD', '')]  # i need the coin without the busd
                print(f' The amount of {selling_coin} is = {amount_of_coin}')
                # we need to check that the amount is bigger than the minimum
                minimum_quantity_for_coin = get_minimum_price(selling_coin)
                variable = math.floor(float(amount_of_coin))
                if amount_of_coin > minimum_quantity_for_coin: # This is with BUSD tag
                    if selling_coin in ['DOGEBUSD', 'SHIBBUSD', 'CAKEBUSD'] and int(variable) > 0:
                        coin_database[selling_coin].Sellers_remorse(int(variable))
                    elif selling_coin in ['DOGEBUSD', 'SHIBBUSD', 'CAKEBUSD']:
                        print("cant sell the coin it is shit \n")
                    else:
                        coin_database[selling_coin].Sellers_remorse(amount_of_coin)  # {'BTC': 0.02}

                else:
                    print(f"couldn't sell the {selling_coin} the amount is too little\n")
            except:
                print(f"Couldn't sell {selling_coin} it isn't listed on the market\n")
    for buying_coin in buyer:
        coin_database[buying_coin].Buyers_regret()
        print(f'BOUGHT {buying_coin} for 30$')
        TOTAL_BALANCE -= 30
    # print(TOTAL_BALANCE)


if __name__ == '__main__':
    main()
