import pandas as pd
import yfinance as yf

# Get the S&P 500 companies list from Wikipedia
url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
smp500_table = pd.read_html(url)[0]

# Extract the ticker symbols
symbols = smp500_table['Symbol'].tolist()

# Display the list of stock symbols
print("S&P 500 Stock Symbols:")
# for symbol in symbols:
#     print(symbol)

# If you'd like to get more information about each symbol, you can use yfinance like so:
sysin = open('input.txt', 'w')
sysin.write('')
sysin.close()
sysin = open('input.txt', 'a')
for symbol in symbols:
    sysin.write(symbol + '\n')