'{:.{}f}'.format(float(amount_of_coin), 4)


TOTAL_BALANCE = 0
message = ""
coin_database = GetValues()  # for example {'BNBBUSD': Stock('BNBBUSD')
desired_coins = Get_buy_appraisal(coin_database)  # for example ['BNBBUSD','ATOMBUSD','ETHBUSD']
message += f'{desired_coins}\n'

owned_coins = GetOwnedAssets()  # for example {'BNB': 0.01, 'ETH':3}

owned_coin_pairs = coin_to_coinBUSD(owned_coins)

for selling_coin in owned_coin_pairs:
 if selling_coin not in coin_database and selling_coin != "BUSDBUSD":
  message += f'The {selling_coin} coin isnt supported\n'
 elif selling_coin in desired_coins:  # if a coin is desired and and is owned
  message += f"Your coin {selling_coin} hasn't been sold cause it is in the desired coins\n"
 elif selling_coin != 'BUSDBUSD' and selling_coin != "USDTBUSD":  # if a coin desired and not owned
  amount_of_coin = owned_coins[selling_coin.replace('BUSD', '')]
  # i need the coin without the busd
  # print(f' The amount of {selling_coin} is = {amount_of_coin}')
  # we need to check that the amount is bigger than the minimum
  minimum_quantity_for_coin = coin_database[selling_coin].get_minimum_price()
  variable = math.floor(float(amount_of_coin))
  if amount_of_coin > minimum_quantity_for_coin:  # This is with BUSD tag
   if selling_coin in ['DOGEBUSD', 'SHIBBUSD', 'CAKEBUSD'] and int(variable) > 1:  # If selling_coin is bigger than 1
    message += coin_database[selling_coin].Sellers_remorse(int(variable))
   elif selling_coin in ['DOGEBUSD', 'SHIBBUSD', 'CAKEBUSD']:
    message += f"cant sell the {selling_coin} it is shit \n"
   else:
    try:
     message += coin_database[selling_coin].Sellers_remorse(
      '{:.{}f}'.format(float(amount_of_coin), 4))  # {'BTC': 0.02}
    except:
     try:
      message += coin_database[selling_coin].Sellers_remorse(variable)
     except Exception as ex:
      message += f"Couldn't sell {variable} units of {selling_coin} {str(ex)}\n"
  else:
   message += f"couldn't sell the {selling_coin} the amount is too little\n"
owned_coins_after_selling = GetOwnedAssets()['BUSD']  # {'BUSD': 134}
# time.sleep(10)  # Debatable if needed
price_for_one_stock = math.floor(float(owned_coins_after_selling) / 3)
if price_for_one_stock > 1:
 for buying_coin in desired_coins:
  if price_for_one_stock >= 10:
   coin_database[buying_coin].Buyers_regret(price_for_one_stock)
   message += f'BOUGHT {buying_coin} for {price_for_one_stock}$\n'
  else:
   print('Something went wrong line 92')
else:
 message += f'insufficient balance didnt enforce desired coins\n'
SendEmailToMKAZ(message)
print(message)