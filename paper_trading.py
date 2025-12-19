import yfinance as yf
import time
import json 
# ticker banaya kyuki ye us stock ka id card hain iski help se wo data lekar ayega wo pura
sbin=yf.Ticker("BTC-USD")
balance=100000
is_stock_held=False
buy_price=0
qty=0
sl_price=0
targetprice=0
print(" HEAVY DRIVER BOT STARTED...")
print(f" Initial Balance: ${balance}")
# Step 2: Loop aur Live Data (Dil ki Dhadkan)
# Ab humein wo loop banana hai jo har minute  market se naya data laaye 

def save_data():
    global balance, qty, buy_price, is_stock_held, sl_price, targetprice
    data={
        "balance":balance,
        "qty":qty,
        "buy_price":buy_price,
        "is_stock_held":is_stock_held,
        "sl_price":sl_price,
        "targetprice":targetprice
    }
    try:
        with open("trade_data.json","w") as f:
            json.dump(data,f)
            print("data saved succesefully")
    except Exception as e:
        print(f"Error saving data {e} ")

def load_data():
    global balance, is_stock_held, buy_price,qty,sl_price,targetprice
    try:
        with open ("trade_data.json","r") as f:
            data=json.load(f)
            balance=data['balance']
            qty=data['qty']
            buy_price=data['buy_price']
            is_stock_held=data["is_stock_held"]
            sl_price=data['sl_price']
            targetprice=data['targetprice']
    except FileNotFoundError as e :
        print(f"Error:--> {e}")


    


def making_decision():
    global balance, is_stock_held, buy_price,qty,sl_price,targetprice
    while True:
        print("checking Market...")

        data = sbin.history(period='1d', interval='1m')
        if len(data)==0:
            print(" Data nahi aaya (Yahoo error). 5 second ruk kar wapas try karenge...")
            time.sleep(5)
            continue
        

        # data=sbin.history(period="1d",interval="1m")
        data['SMA5']=data['Close'].rolling(window=5).mean()
        current_price=data["Close"].iloc[-1]
        current_sma=data["SMA5"].iloc[-1]

        print(f"Price: {round(current_price,2)} | SMA: {round(current_sma,2)}")
        if current_price > current_sma and is_stock_held == False :
            print("BUY MARKET IS HIGH")
            qty = int(balance / current_price)
            cost = qty * current_price
            balance=balance-cost
            is_stock_held=True
            buy_price = current_price
            print(f"Bought {qty} shares @ ${round(current_price, 2)}")
            print(f" Wallet Balance: ${round(balance, 2)}")
            sl_price=buy_price-(buy_price*0.01)
            targetprice=buy_price+(buy_price*0.02)
            save_data()

        elif is_stock_held == True:
            if (current_price <= sl_price):
                print("stop loss is hitting ")
                print("SELL MARKET IS LOW")
                sell_value = qty * current_price
                balance = balance + sell_value
                total_profit = (current_price - buy_price) * qty
                is_stock_held=False
                qty = 0
                # profit/loss
                print(f"Sold all shares @ ${round(current_price, 2)}")
                print(f"Total Profit/Loss: ${round(total_profit, 2)}")
                print(f"New Wallet Balance: ${round(balance, 2)}")
                save_data()

            elif  (current_price >=targetprice):
                print("target hit earned money")
                print("SELL MARKET IS LOW")
                sell_value = qty * current_price
                balance = balance + sell_value
                total_profit = (current_price - buy_price) * qty
                is_stock_held=False
                qty = 0
                # profit/loss
                print(f"Sold all shares @ ${round(current_price, 2)}")
                print(f" Total Profit/Loss: ${round(total_profit, 2)}")
                print(f"New Wallet Balance: ${round(balance, 2)}")
                save_data()

            elif current_price<current_sma :
                print("SELL MARKET IS LOW")
                sell_value = qty * current_price
                balance = balance + sell_value
                total_profit = (current_price - buy_price) * qty
                is_stock_held=False
                qty = 0
                # profit/loss
                print(f" Sold all shares @ ${round(current_price, 2)}")
                print(f" Total Profit/Loss: ${round(total_profit, 2)}")
                print(f" New Wallet Balance: ${round(balance, 2)}")
                save_data()

            else :
                current_value = current_price * qty
                buy_value = buy_price * qty
                unrealized_pnl = current_value - buy_value
                print(f"HOLDING {qty} Shares... (SL: {round(sl_price,2)} | TP: {round(targetprice,2)})")
                print(f"   Abhi ka Status: ${round(unrealized_pnl, 2)} (Agar abhi becha toh)")
                

        else:
                print(" Kuch nahi karna (Waiting...)")

        print("Waiting 60 seconds...")
        time.sleep(60)

load_data()

making_decision()
