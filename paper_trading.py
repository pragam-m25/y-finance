import yfinance as yf
import time
# ticker banaya kyuki ye us stock ka id card hain iski help se wo data lekar ayega wo pura
sbin=yf.Ticker("SBIN.NS")
balance=10000
is_stock_held=False
# Step 2: Loop aur Live Data (Dil ki Dhadkan)
# Ab humein wo loop banana hai jo har minute  market se naya data laaye 
def making_decision():
    while True:
        print("checking Market...")
        data=sbin.history(period="1d",interval="1m")
        data['SMA5']=data['close'].rolling(window=5).mean()
        current_price=data["close"].iloc[-1]
        current_sma=data["SMA5"].iloc[-1]
        
        print(f"Price: {current_price} | SMA: {current_sma}")