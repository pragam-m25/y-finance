import yfinance as yf
sbin=yf.Ticker("SBIN.NS")
data=sbin.history(period='1mo')
# print(data)
average_price=data['Close'].mean()
print(average_price)
