# Raw Package
import numpy as np
import pandas as pd

#Data Source
import yfinance as yf

#Data viz
import plotly.graph_objs as go

#Interval required 1 minute
data1 = yf.download(tickers='MSFT', period='1d', interval='1m')
data2 = yf.download(tickers='AAPL', period='1d', interval='1m')

#declare figure
fig = go.Figure()

#Candlestick
fig.add_trace(go.Candlestick(x=data1.index,
                open=data1['Open'],
                high=data1['High'],
                low=data1['Low'],
                close=data1['Close'], name = 'MSFT'))
fig.add_trace(go.Candlestick(x=data2.index,
                open=data2['Open'],
                high=data2['High'],
                low=data2['Low'],
                close=data2['Close'], name = 'AAPL'))

# Add titles
fig.update_layout(
    title='AAPL vs MSFT price',
    yaxis_title='Stock Price (%)')

# X-Axes
fig.update_xaxes(
    rangeslider_visible=True,
    rangeselector=dict(
        buttons=list([
            dict(count=15, label="15m", step="minute", stepmode="backward"),
            dict(count=45, label="45m", step="minute", stepmode="backward"),
            dict(count=1, label="HTD", step="hour", stepmode="todate"),
            dict(count=3, label="3h", step="hour", stepmode="backward"),
            dict(step="all")
        ])
    )
)

#Show
fig.show()
