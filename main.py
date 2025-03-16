import yfinance as yf
import pandas as pd
import backtrader as bt
from datetime import datetime

class MomentumStrategy(bt.Strategy):
    params = (('rsi_period', 14), ('macd_fast', 12), ('macd_slow', 26), ('macd_signal', 9))

    def __init__(self):
        self.rsi = bt.indicators.RSI(period=self.params.rsi_period)
        self.macd = bt.indicators.MACD(fast=self.params.macd_fast, slow=self.params.macd_slow, signal=self.params.macd_signal)

    def next(self):
        if not self.position:
            if self.rsi < 30 and self.macd.macd > self.macd.signal:
                self.buy()
            elif self.rsi > 70 and self.macd.macd < self.macd.signal:
                self.sell()

# Fetch stock data
def get_stock_data(symbol, start='2025-01-01', end=None):
    if end is None:
        end = datetime.today().strftime('%Y-%m-%d')
    data = yf.download(symbol, start=start, end=end, auto_adjust=False)
    
    # Ensure the required columns are present
    data = data[['Open', 'High', 'Low', 'Close', 'Volume']]
    data.index.name = 'Date'
    data.to_csv(f'./csv_files/{symbol}.csv', index=True)
    
    return f'./csv_files/{symbol}.csv'

# Buy/Sell Decision Function
def should_buy_stock(csv_file):
    data = pd.read_csv(csv_file, index_col='Date', parse_dates=True)
    data['RSI'] = data['Close'].rolling(14).apply(lambda x: 100 - (100 / (1 + (x[-1] - x[:-1].mean()) / x[:-1].std())))
    data['MACD'] = data['Close'].ewm(span=12, adjust=False).mean() - data['Close'].ewm(span=26, adjust=False).mean()
    data['Signal'] = data['MACD'].ewm(span=9, adjust=False).mean()
    
    latest = data.iloc[-1]
    
    if latest['RSI'] < 30 and latest['MACD'] > latest['Signal']:
        return "Buy"
    elif latest['RSI'] > 70 and latest['MACD'] < latest['Signal']:
        return "Sell"
    else:
        return "Hold"

# Backtesting function
def backtest_strategy(csv_file):
    cerebro = bt.Cerebro()
    data = bt.feeds.GenericCSVData(
        dataname=csv_file,
        dtformat='%Y-%m-%d',
        timeframe=bt.TimeFrame.Days,
        compression=1,
        openinterest=-1,
        headers=True
    )
    cerebro.adddata(data)
    cerebro.addstrategy(MomentumStrategy)
    cerebro.run()
    cerebro.plot()

if __name__ == "__main__":
    out = open('output.txt', 'w')
    out.write('')
    out.close()
    out = open('output.txt', 'a')
    decisions = []
    for stock in open('input.txt', 'r').readlines():
        stock = stock.strip()
        stock_csv = get_stock_data(stock)  # Example: Apple stock
        stock_csv = open(f'./csv_files/{stock}.csv', 'r')
        lines = stock_csv.readlines()
        lines.pop(1)
        lines.pop(1)
        lines[0] = 'Date,Open,High,Low,Close,Volume'
        stock_csv.close()
        stock_csv = open(f'./csv_files/{stock}.csv', 'w')
        stock_csv.writelines(lines)
        stock_csv.close()
        stock_csv = open(f'./csv_files/{stock}.csv', 'r')
        out.write(f'Decision for {stock}: ' + should_buy_stock(stock_csv) + '\n')