import yfinance as yf
import matplotlib.pyplot as plt


test_file = 'D:\code\utils\stonk\info\ amzn\2022.02.18_23.16.44\1d.price'
with open(test_file, 'r') as f:
    test = f.read()
print(test)
# get stock info
#for key in msft.info:
    #try:
    #    int(msft.info[key])
    #    print('%s %s' % (key, msft.info[key]))
    #except:
#        pass

# get historical market data
#hist = msft.history(period="1mo")
#hist.plot()
#plt.show()
#for item in dir(msft):
    #try:
    #    print('%s %s' % (item, eval("msft.%s" % item)))
    #except:
#        pass

# # show actions (dividends, splits)
# print(msft.actions)
#
# # show dividends
# print(msft.dividends)
#
# # show splits
# print(msft.splits)
#
# # show financials
# print(msft.financials)
# print(msft.quarterly_financials)
#
# # show major holders
# print(msft.major_holders)
#
# # show institutional holders
# print(msft.institutional_holders)
#
# # show balance sheet
# print(msft.balance_sheet)
# print(msft.quarterly_balance_sheet)
#
# # show cashflow
# print(msft.cashflow)
# print(msft.quarterly_cashflow)
#
# # show earnings
# print(msft.earnings)
# print(msft.quarterly_earnings)
#
# # show sustainability
# print(msft.sustainability)
#
# # show analysts recommendations
# #print(msft.recommendations)
#
# # show next event (earnings, etc)
# print(msft.calendar)
#
# # show ISIN code - *experimental*
# # ISIN = International Securities Identification Number
# print(msft.isin)
#
# # show options expirations
# print(msft.options)
#
# # get option chain for specific expiration
# opt = msft.option_chain('2021-08-06')
# # data available via: opt.calls, opt.puts
#
# tickers = yf.Tickers('msft aapl goog')
# # ^ returns a named tuple of Ticker objects
#
#
# data = yf.download(  # or pdr.get_data_yahoo(...
#     # tickers list or string as well
#     tickers="SPY AAPL MSFT",
#
#     # use "period" instead of start/end
#     # valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
#     # (optional, default is '1mo')
#     period="ytd",
#
#     # fetch data by interval (including intraday if period < 60 days)
#     # valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
#     # (optional, default is '1d')
#     interval="1d",
#
#     # group by ticker (to access via data['SPY'])
#     # (optional, default is 'column')
#     group_by='ticker',
#
#     # adjust all OHLC automatically
#     # (optional, default is False)
#     auto_adjust=True,
#
#     # download pre/post regular market hours data
#     # (optional, default is False)
#     prepost=True,
#
#     # use threads for mass downloading? (True/False/Integer)
#     # (optional, default is True)
#     threads=True,
#
#     # proxy URL scheme use use when downloading?
#     # (optional, default is None)
#     proxy=None
# )
