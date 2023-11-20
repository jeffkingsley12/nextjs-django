from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from .models import Transaction, Balance, Trade
import time
from binance.client import Client
from binance.enums import SIDE_BUY, SIDE_SELL, TIME_IN_FORCE_GTC
from django.http import JsonResponse

import requests  # Add this line to import the requests module

# Replace with your Binance API credentials
API_KEY = '4XxLXXiPSNTAofTWRt8Dfimv2ZkpDzoR7UjSHZqPU7X2jiOAOOtCwnviE1lYY7Od'
SECRET_KEY = 'yX1F4s6KDTh8MrSZelnZPal0B1nNKCDNoHjOpkSANPnxaZNY2Vl19icxY9g3o51A'

# Replace with your preferred cryptocurrency pair, e.g., 'BTCUSDT'
SYMBOL = 'DOGEUSD'

BASE_URL = 'https://api.binance.com/api/v3'

# Simple moving average (SMA) parameters
SHORT_PERIOD = 20
LONG_PERIOD = 50

# Percentage threshold for buy/sell signals
BUY_THRESHOLD = 0.01  # 1%
SELL_THRESHOLD = -0.01  # -1%

# Initialize Binance API client
client = Client(API_KEY, SECRET_KEY)

# Function to get the SMA of the specified period
def get_sma(data, period):
    return sum(data[-period:]) / float(period)


# Function to fetch historical klines (candlestick data) from Binance API
def fetch_historical_klines(symbol, interval, limit=1000):
    url = f'{BASE_URL}/klines'
    params = {
        'symbol': symbol,
        'interval': interval,
        'limit': limit
    }
    response = requests.get(url, params=params)
    candles = response.json()
    return [float(candle[4]) for candle in candles]  # Use closing price (index 4)



# ... (previous code remains unchanged)

# Function to analyze the trading pairs
def analyze(pairs):
    # Initialize an empty list to store the signal coins
    signal_coins = []

    for pair in pairs:
        symbol = f"{pair}USDT"  # Assuming all pairs are against USDT
        trading_mode = TradingMode(symbol, MY_EXCHANGE, MY_SCREENER)
        first_analysis = trading_mode.analyze_ticker(MY_FIRST_INTERVAL)
        second_analysis = trading_mode.analyze_ticker(MY_SECOND_INTERVAL)

        first_tacheck = first_analysis[0]
        second_tacheck = second_analysis[0]

        if first_tacheck >= TA_BUY_THRESHOLD and second_tacheck >= TA_BUY_THRESHOLD:
            signal_coins.append(pair)

    return signal_coins

# Function to execute a buy order
def execute_buy_order(amount):
    # Add the buy order execution logic here
    ...

    # Update the balance and store the transaction
    balance = Balance.objects.first()
    balance.amount += amount
    balance.save()

    Transaction.objects.create(
        symbol=SYMBOL,
        price=latest_price,
        quantity=amount / latest_price
    )

# Function to execute a sell order
def execute_sell_order(quantity):
    # Add the sell order execution logic here
    ...

    # Update the balance and store the transaction
    balance = Balance.objects.first()
    balance.amount -= quantity * latest_price
    balance.save()

    Transaction.objects.create(
        symbol=SYMBOL,
        price=latest_price,
        quantity=-quantity
    )

# View to handle trading signals
def trading_view(request):
    # Initialize the balance (if not already present)
    if not Balance.objects.exists():
        Balance.objects.create(amount=100.0)

    while True:
        # Fetch the list of trading pairs from Binance
        exchange_info = client.get_exchange_info()
        pairs = [symbol_info['symbol'][:-4] for symbol_info in exchange_info['symbols'] if symbol_info['quoteAsset'] == 'USDT']

        if signal_coins := analyze(pairs):
            for _ in signal_coins:
                execute_buy_order(6.0)  # Buy assets worth 6 USD for each signal coin

        # Wait for some time before checking again (adjust the interval as per your preference)
        time.sleep(60)

    return HttpResponse("Trading signals monitoring started.")
    
def transaction_history_view(request):
    # Fetch all transactions from the database
    transactions = Transaction.objects.all()

    # Fetch the current balance from the database
    balance = Balance.objects.first()

    # Pass the data to the template for rendering
    context = {
        'transactions': transactions,
        'balance': balance,
    }

    return render(request, 'transaction_history.html', context)
    


def save_trade_data(request, symbol):
    url = f'https://api.binance.us/api/v3/trades?symbol={symbol}'

    resp = requests.get(url)

    if resp.status_code != 200:
        return JsonResponse({'error': 'Failed to fetch trades data'}, status=resp.status_code)
    trades_data = resp.json()
    for trade_data in trades_data:
        trade = Trade(
            trade_id=trade_data['id'],
            price=trade_data['price'],
            quantity=trade_data['qty'],
            quote_quantity=trade_data['quoteQty'],
            timestamp=trade_data['time'],
            is_buyer_maker=trade_data['isBuyerMaker'],
            is_best_match=trade_data['isBestMatch'],
            symbol=symbol
        )
        trade.save()

    return JsonResponse({'message': 'Trades data saved successfully!'})
