#revision 2022-02-08 logging print line add.

import time
import pyupbit
import datetime

access = ""
secret = ""

def get_target_price(ticker, k):
    """target price for buying following strategy"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price

def get_start_time(ticker):
    """get start time"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time

def get_balance(ticker):
    """get balance money"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0

def get_current_price(ticker):
    """get current price"""
    return pyupbit.get_orderbook(ticker=ticker)["orderbook_units"][0]["ask_price"]

# log-in
upbit = pyupbit.Upbit(access, secret)
print("autotrade start. current time: ",datetime.datetime.now())

# auto trading start
while True:
    try:
        now = datetime.datetime.now()
        start_time = get_start_time("KRW-ETH") #9:00
        end_time = start_time + datetime.timedelta(days=1) #9:00 + 1day

        if start_time < now < end_time - datetime.timedelta(seconds=36): #JWC( seconds=36 )
            target_price = get_target_price("KRW-ETH", 0.3) # K= 0.3
            current_price = get_current_price("KRW-ETH")
            if target_price < current_price:
                krw = get_balance("KRW")
                if krw > 1000000:                                   #when balance is bigger than 1,000,000
                    print("#########################################")
                    print("now: ",now)
                    print("current price is higher than target price")
                    print("target price: ",target_price,"   current price: ",current_price)
                    print("!!make buy_market_order!!")
                    upbit.buy_market_order("KRW-ETH", krw-1000000)  #balance - 1,000,000 buy order
                    print("!!buy_market_order *DONE*!!")
                    print("#########################################")
        else:
            ethnumber = get_balance("ETH")                          #ethnumber variable editted.
            if ethnumber > 1:                                       # when the ether number is bigget than 1
                print("################################")
                print("!!make sell order")
                upbit.sell_market_order("KRW-ETH", ethnumber-1)
                print("!!sell order *Done*!!, ether numbers: ", ethnumber-1)
                print("now: ", now)
                print("################################")
        time.sleep(3)
    except Exception as e:
        print(e)
        time.sleep(1)