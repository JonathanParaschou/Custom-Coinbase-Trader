import cbpro
import pandas as pd
import plotly.graph_objects as go
import requests

c = cbpro.PublicClient()

data = pd.DataFrame(c.get_products())
data.tail().T

##Testing Area

#Getting Price Data
ticker = c.get_product_ticker(product_id='ETH-USD')
print(ticker)
print()

#Pulling Historical Data
historical = pd.DataFrame(c.get_product_historic_rates(product_id='ETH-USD'))
historical.columns= ["Date","Open","High","Low","Close","Volume"]
historical['Date'] = pd.to_datetime(historical['Date'], unit='s')
historical.set_index('Date', inplace=True)
historical.sort_values(by='Date', ascending=True, inplace=True)
print(historical)
print()

#Technical Indicators
historical['20 SMA'] = historical.Close.rolling(20).mean()
print(historical.tail())
print()

#Making a Graph with Historical Data
fig = go.Figure(data=[go.Candlestick(x = historical.index,
                                    open = historical['Open'],
                                    high = historical['High'],
                                    low = historical['Low'],
                                    close = historical['Close'],
                                    ),
                     go.Scatter(x=historical.index, y=historical['20 SMA'], line=dict(color='purple', width=1))])


#fig.show()

#Order Book Data
order_book = c.get_product_order_book('BTC-USD')
order_book

bids = pd.DataFrame(order_book['bids'])
asks = pd.DataFrame(order_book['asks'])

df = pd.merge(bids, asks, left_index=True, right_index=True)
df = df.rename({"0_x":"Bid Price","1_x":"Bid Size", "2_x":"Bid Amount",
                "0_y":"Ask Price","1_y":"Ask Size", "2_y":"Ask Amount"}, axis='columns')
print(df.head())
print()


#Trade Data
trades = pd.DataFrame(requests.get('https://api.pro.coinbase.com/products/ETH-USD/trades').json())
print(trades.tail())