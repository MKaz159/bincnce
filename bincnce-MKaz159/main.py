# import time
import time
import sys
from stockfunctions import *
from pprint import pprint


# Function to convert to BNB the assets that can't be sold
def GetDustAssets():
    ''' Returns the assets that can be converted to BNB at the end
    :return: 'ATOM,BUSD,SAND'
    '''
    returned_dust_assets = []
    multiple_dictionary = client.get_dust_assets(recvWindow=59000)
    assets_dictionary = multiple_dictionary['details']
    res = len([ele for ele in assets_dictionary if isinstance(ele, dict)])
    for i in range(0, res):
        returned_dust_assets.append(assets_dictionary[i]['asset'])
    final_string = ','.join(returned_dust_assets)
    return final_string


# Function to convert to BNB the assets that can't be sold


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


# When the calculation occurs
def coin_to_coinBUSD(owned_coins):
    coin_with_BUSD = []
    BUSD_with_coin = owned_coins.keys()
    for coin in BUSD_with_coin:
        coin_with_BUSD.append(coin + 'BUSD')
    return coin_with_BUSD


# A list of coins meant to be sold
def Coins_to_sell(buy_target, assets):
    '''
    :param buy_target: ['ETHBUSD', 'BNBBUSD', 'SOLBUSD']
    :param assets: {'BTC':0.01,'ETH':0.1,'BUSD':143}
    :return: ['MATICBUSD','ATOMBUSD'] The coins in assets but not in buy target
    '''
    coins_to_sell = []
    # Don't want to sell BUSD
    if 'BUSD' in assets: del assets['BUSD']
    # Constructing the coins_to_sell list
    for asset in assets:
        if any(asset in string for string in buy_target):
            continue
        else:
            coins_to_sell.append(f'{asset}BUSD')
    return coins_to_sell

#Get_buy_appraisal(GetValues)
def main():
    with open('Script results.txt', 'a') as result_file:
        result_file.write(f"\n          {datetime.today().strftime('%Y-%m-%d')}\n")
        ticker_to_coinDB = GetValues()  # for example {'BNBBUSD': Stock('BNBBUSD')}
        assets_before_selling = GetOwnedAssets()  # for example {'BTC':0.01,'ETH':0.1}
        buy_target = Get_buy_appraisal(ticker_to_coinDB)  # for example ['ETHBUSD', 'BNBBUSD', 'SOLBUSD']
        sales_departement = Coins_to_sell(buy_target, assets_before_selling)  # for example ['ATOMBUSD', 'SANDBUSD']
        result_file.write(f'Bulls recommend a move on {buy_target}\n')

        # SALES FORCE #
        if len(sales_departement) == 0:
            result_file.write(f'recommended assets are already owned')
        else:
            result_file.write('\n sales force initiated\n')
            for seller_coin in sales_departement:
                amount = assets_before_selling[
                    seller_coin.replace('BUSD', '')]  # we need to pass the seller_coin without BUSD for the amount
                try:
                    result_file.write(f'Attempting to sell {seller_coin} with amount of {amount}\n')
                    seller_stock_class = ticker_to_coinDB[seller_coin]  # Getting "Stock(seller_coin)"
                    result = seller_stock_class.Sellers_remorse(amount)
                    result_file.write(result)
                except Exception as ex:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    result_file.write(exc_type, fname, exc_tb.tb_lineno)
        # SALES FORCE#

        # BUSD ASSET CALCULATION #
        assets_after_sell = GetOwnedAssets()
        try:
            amount_BUSD = assets_after_sell['BUSD']
            amount_of_stocks_to_buy = len(buy_target)
            amount_BUSD_each_stock = float(amount_BUSD) / amount_of_stocks_to_buy
            result_file.write(f'\nAmount purchase for each asset {amount_BUSD}$\n')
            if float(amount_BUSD) < 10.0:
                result_file.write(f'\n Amount of BUSD is under 10$ BUSD = {amount_BUSD} worthless')
                amount_BUSD = 0
        except:
            result_file.write('No BUSD in the bank')
            amount_BUSD = 0
            amount_BUSD_each_stock = 0
            result_file.write(f'\n No BUSD in the Bank Bulls not initiated\n')
        # BUSD ASSET CALCULATION #

        # Bulls #
        if amount_BUSD_each_stock < 10.0 and amount_BUSD != 0:
            try:
                result_file.write(f'Attempting to purchase {buy_target[0]} for {amount_BUSD}$\n')
                buying_stock = ticker_to_coinDB[buy_target[0]]
                result_file.write(buying_stock.Buyers_regret(amount_BUSD))
            except Exception as ex:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                result_file.write(exc_type, fname, exc_tb.tb_lineno)
        elif amount_BUSD != 0:
            for buying_coin in buy_target:
                try:
                    result_file.write(f'Attempting to purchase {buying_coin} for {amount_BUSD_each_stock}$\n')
                    buyer_stock = ticker_to_coinDB[buying_coin]
                    result_file.write(buyer_stock.Buyers_regret(amount_BUSD_each_stock))
                    # result_file.write(f'Bought {buying_coin} for {amount_BUSD}$\n')
                except Exception as e:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    result_file.write(exc_type, fname, exc_tb.tb_lineno)
        # Bulls #

        # Convertion to BNB #
        assets_to_be_converted = GetDustAssets()
        if assets_to_be_converted == '':
            pass
        else:
            client.transfer_dust(recvWindow=59000, asset=assets_to_be_converted)
        # Convertion to BNB #


if __name__ == '__main__':
    pprint(GetOwnedAssets())
    main()
    # time.sleep(60)
    pprint(GetOwnedAssets())
    # time.sleep(60)
    #sys.exit()
