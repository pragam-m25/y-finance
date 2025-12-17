import yfinance as yf
import time 
sbin=yf.Ticker("SBIN.NS")
# data=sbin.history(period='1mo')
# print(data)
# average_price=data['Close'].mean()
# print(average_price)
# data['SMA_5']=data['Close'].rolling(window=5).mean()
# print(data['SMA_5'])
# kaise hum latest day ka price nikale 
# current_price=data['Close'].iloc[-1]
'''
data['Close']: Humne puri table mein se sirf 'Close' price wali line uthayi.

.iloc: Humne kaha "Mujhe specific location par jana hai."

[-1]: Humne kaha "Last wala de." (Agar -2 likhte toh kal ka milta, -3 likhte toh parso ka).
'''
def checking_buyorsell():
    while True:
        print("\n checking for new data ")

        data=sbin.history(period='1mo')

        data['SMA_5']=data['Close'].rolling(window=5).mean()

        current_price=data['Close'].iloc[-1]#ye current price nikalega 
        current_price_sma5=data['SMA_5'].iloc[-1]#ye last 5 days ka moving average nikalega 

        print(f"price:{current_price}|SMA:{current_price_sma5}")
        if current_price > current_price_sma5:
            print("market is high ,buy karo trend follow")
        else:
            print("market is low ,sell trend stop")
        
        print("Waiting for 60 seconds...")
        time.sleep(60)#ye code execution ko pause karega 60 seconds ke liye

# checking_buyorsell()