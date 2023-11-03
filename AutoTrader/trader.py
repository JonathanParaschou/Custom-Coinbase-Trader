from tkinter.constants import LEFT, RIGHT
import coinbase
from coinbase.wallet.client import Client
import json
import pandas as pd
import plotly.graph_objects as go
import tkinter as tk
import requests
import time
from time import sleep
from six import add_move

##Key Phrase Imports
key = ''
secret = ''
client = Client(key, secret)

##Polling Bitcoin Wallet Data
def bit_walletBalance():
    account = client.get_account('BTC')
    account.refresh
    return(account['native_balance']['amount'])

##Polling Dollar Wallet Data
def usd_walletBalance():
    account = client.get_account('USD')
    account.refresh
    return(account['native_balance']['amount'])

##Polling Bitcoin Market Price
def bitPrice(): 
    response = requests.get('https://api.coindesk.com/v1/bpi/currentprice.json')
    data = response.json()
    return(data['bpi']['USD']['rate'])

def sell_bit():
    account = client.get_account('BTC')
    id = account['id']
    client.sell(id, amount='0.00016', currency='BTC')

def buy_bit():
    account = client.get_account('BTC')
    id = account['id']
    client.buy(id, amount='0.00016', currency='BTC')

##GUI Setup w/ Tkinter
def GUI():
    def buyText():
        print("Bought")
    def sellText():
        print("Sold")
    window = tk.Tk()
    frame1 = tk.Frame()
    frame2 = tk.Frame()
    frame3 = tk.Frame()
    label1 = tk.Label(master=frame1, width=61, height=10, text="CoinBase Info", bg='blue', fg='white')
    bit_balanceLabel = tk.Label(master=frame2, width=20, height=10, text="Bitcoin Wallet Balance: "+bit_walletBalance(), bg='gold')
    usd_balanceLabel = tk.Label(master=frame2, width=20, height=10, text="USD Wallet Balance: "+usd_walletBalance(), bg='cyan')
    priceLabel = tk.Label(master=frame2, width=20, height=10, text="Bitcoin Price: "+bitPrice(), bg='gold')
    buyButton = tk.Button(master=frame3, width=30, height=10, text="Buy", command=lambda:[buyText()], bg='green')
    sellButton = tk.Button(master=frame3, width=30, height=10, text="Sell", command=lambda:[sellText()], bg='red')    
    label1.pack()
    bit_balanceLabel.pack(side=LEFT)
    usd_balanceLabel.pack(side=LEFT)
    priceLabel.pack(side=RIGHT)
    buyButton.pack(side=LEFT)
    sellButton.pack(side=RIGHT)
    frame1.pack()
    frame2.pack()
    frame3.pack()
    def update():
        bit_balanceLabel['text'] = "Bitcoin Wallet Balance: "+bit_walletBalance()
        usd_balanceLabel['text'] = "USD Wallet Balance: "+usd_walletBalance()
        priceLabel['text'] = "Bitcoin Price: "+bitPrice()
        window.after(5000, update)
    update()
    window.mainloop()



##Actual Trading Algrothim
def tradingAlgo():
    heldPrice = bitPrice()
    time.sleep(30)
    currentPrice = bitPrice()
    if(currentPrice<=(0.95*heldPrice)):
        buy_bit()
        print("Bought for "+currentPrice)
    if(currentPrice>=1.05*heldPrice):
        sell_bit()
        print("Sold for "+currentPrice)

GUI()
    