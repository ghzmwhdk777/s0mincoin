import time
import pyupbit
import datetime

access = ""
secret = ""

def get_target_price(ticker, k):

    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price

def get_start_time(ticker):

    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time

def get_balance(ticker):

    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0

def get_current_price(ticker):

    return pyupbit.get_orderbook(ticker=ticker)["orderbook_units"][0]["ask_price"]


upbit = pyupbit.Upbit(access, secret)
print("autotrade start")


while True:
    try:
        now = datetime.datetime.now()
        start_time = get_start_time("KRW-ETH")
        end_time = start_time + datetime.timedelta(days=1)

        if start_time < now < end_time - datetime.timedelta(seconds=10):
            target_price = get_target_price("KRW-ETH", 0.5)
            current_price = get_current_price("KRW-ETH")
            if target_price < current_price:
                krw = get_balance("ETH")
                if krw > 5000:
                    upbit.buy_market_order("KRW-ETH", krw*0.9995)
        else:
            btc = get_balance("ETH")
            if btc > 0.00008:
                upbit.sell_market_order("KRW-ETH", btc*0.9995)
        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)
