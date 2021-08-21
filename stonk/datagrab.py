import os
import pathlib
import yfinance as yf
import matplotlib.pyplot as plt
import json
import datetime
time_format = '%Y.%m.%d_%H.%M.%S'
now = datetime.datetime.now()
now_s = now.strftime(time_format)

def set_nums(ticker, symbol):
    with open(r'info\%s\%s\nums' % (symbol, now_s), 'w') as numeric_file:
        for key in ticker.info:
            try:
                int(ticker.info[key])
                numeric_file.write('%s %s\n' % (key, ticker.info[key]))
            except Exception as ex:
                pass

def set_ticker(ticker, symbol):
    with open(r'info\%s\%s\ticker' % (symbol, now_s), 'w') as ticker_file:
        for item in dir(ticker):
            try:
                ticker_file.write('%s %s\n' % (item, eval("ticker.%s" % item)))
            except Exception as ex:
                print(ex)

def set_history(ticker: yf.Ticker, symbol:str):
    periods = {'1d':'1m', '5d':'5m', '1mo':'15m', '3mo':'1h', '6mo':'1h', '1y':'1d', '2y':'1d', '5y':'1d', '10y':'1wk','ytd':'1d'}
    for period in periods.keys():
        interval = periods[period]
        try:
            hist = ticker.history(period=period, interval=interval)
            with open(r'info\%s\%s\%s.price' % (symbol, now_s, period), 'w') as price_file:
                    price_file.write('%s' % hist.to_csv())
        except Exception as ex:
            print('%s %s %s' % (period, interval, ex))

def has_todays_data(symbol):
    found = False
    if os.path.isdir('info\%s' % symbol):
        for time_fname in os.listdir('info\%s' % symbol):
            fdate = datetime.datetime.strptime(time_fname, time_format)
            if fdate.date() == now.date():
                print('skipped %s has today\'s data' % symbol)
                found = True
                break
    return found

with open("portfolio.json", 'r') as f:
    folio = json.load(f)
    for symbol in folio.keys():
        if not has_todays_data(symbol):
            ticker = yf.Ticker(symbol)
            pathlib.Path('info\%s\%s' % (symbol,now_s)).mkdir(parents=True, exist_ok=True)
            set_nums(ticker, symbol)
            set_ticker(ticker, symbol)
            set_history(ticker, symbol)
