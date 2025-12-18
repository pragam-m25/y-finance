import yfinance as yf
import time
# ticker banaya kyuki ye us stock ka id card hain iski help se wo data lekar ayega wo pura
sbin=yf.Ticker("SBIN.NS")
balance=10000
is_stock_held=False
buy_price=0
# Step 2: Loop aur Live Data (Dil ki Dhadkan)
# Ab humein wo loop banana hai jo har minute  market se naya data laaye 
def making_decision():
    global balance, is_stock_held, buy_price
    while True:
        print("checking Market...")
        if len(data)==0:
            print("⚠️ Data nahi aaya (Yahoo error). 5 second ruk kar wapas try karenge...")
            time.sleep(5)
            continue
        

        data=sbin.history(period="1d",interval="1m")
        data['SMA5']=data['Close'].rolling(window=5).mean()
        current_price=data["Close"].iloc[-1]
        current_sma=data["SMA5"].iloc[-1]

        print(f"Price: {round(current_price,2)} | SMA: {round(current_sma,2)}")
        if current_price > current_sma and is_stock_held == False :
            print("BUY MARKET IS HIGH")
            balance=balance-current_price
            is_stock_held=True
            buy_price = current_price
            print(f"New Balance: {round(balance, 2)}")
        elif current_price<current_sma and is_stock_held == True:
            print("SELL MARKET IS LOW")
            balance=balance+current_price
            is_stock_held=False
            # profit/loss
            pnl = current_price - buy_price
            print(f"Profit/Loss: {round(pnl, 2)}")
            print(f"New Balance: {round(balance, 2)}")

        else:
            print("⚪ Kuch nahi karna (Waiting...)")

        print("Waiting 60 seconds...")
        time.sleep(60)

making_decision()