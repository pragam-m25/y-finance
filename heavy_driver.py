import yfinance as yf
import pandas as pd 
import json
import os
import csv
from datetime import datetime
import time
TICKER_Name = "BTC-USD"
buffer_percentage=0.0000
Retry_time=5
STOP_LOSS_PERCENTAGE = 0.01  
TARGET_PERCENTAGE = 0.02    
RSI_PERIOD = 14  # RSI 14 candles ka average lega
RSI_OVERBOUGHT = 70 # Isse upar khareedna mana hai 

def time_check():
    """
    ye check karega ki ajj sunday ya saturday to nahi hain ,ya fhir time to nahi hogya market close karneka 
    """
    now=datetime.now()
    current_time=now.time()
    day_name=now.strftime("%A")

    if day_name == "Saturday" or  day_name == "Sunday": 
        return False,"today is weekend "
    
    market_start = datetime.strptime("09:15", "%H:%M").time()
    market_end = datetime.strptime("15:30", "%H:%M").time()


    if market_start <= current_time and current_time <= market_end:
        return True ,"Market is open"
    else:
        return False ,"market is closed "


def load_data():
    if os.path.exists("trade_data.json"):
        with open("trade_data.json","r") as f:
            data= json.load(f)
            if 'buy_price' not in data:
                data['buy_price'] = 0.0
            return data
         
    else:
        return {
            "balance": 100000,
            "qty": 0,
            "buy_price": 0.0  
        }
def save_data(data):
    '''
    ye data save karega humara jo bhi balance wagera hoga usko json ki madat se dictionary ki form mein store karega jab buy/sell karega tab isko call karenge to ye use save karta rahega  
    '''
    with open("trade_data.json", "w") as f: 
        json.dump(data, f)

def log_trade(action, price, quantity, balance, reason):
    file_exists = os.path.isfile("trade_history.csv")
    
    with open("trade_history.csv", "a", newline='') as f:
        writer = csv.writer(f)
        # Agar file nahi hai, toh Header likho
        if not file_exists:
            writer.writerow(["Date", "Time", "TICKER", "Action", "Price", "Qty", "Balance", "Reason"])
        
        now = datetime.now()
        writer.writerow([
            now.strftime("%Y-%m-%d"),
            now.strftime("%H:%M:%S"),
            TICKER_Name,
            action,
            price,
            quantity,
            balance,
            reason
        ])
    print(f" Trade Logged in Excel: {action} at {price}")

# ---  RSI CALCULATION  ---
def calculate_rsi(data, period=14):
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

wait_time = Retry_time

def my_bot():
    print("HEAVY DRIVER BOAT IS STARTED .........")
    wait_time=Retry_time

    wallet = load_data()
    print(f"Initial Balance: {wallet['balance']}")

    while True :
        is_open,status=time_check()

        print(f"market_status:{status}")

        # if not is_open :
        #     time.sleep(60)
        #     continue

        print("market is open fetching the data ")

        try:
            print("heavy driver bot is started ")

            wallet = load_data()
            print(f"Initial Balance: {wallet['balance']}")

            stock=yf.Ticker(TICKER_Name)
            data=stock.history(period='1d', interval='1m')

            if len(data) < RSI_PERIOD:
                print("Not enough data for RSI... waiting")
                time.sleep(5)
                continue

            current_price=data['Close'].iloc[-1]
            data['SMA']=data["Close"].rolling(window=5).mean()
            SMA=data["SMA"].iloc[-1]


            # Calculate RSI
            data['RSI'] = calculate_rsi(data, RSI_PERIOD)
            RSI = data['RSI'].iloc[-1]

            if pd.isna(SMA) or pd.isna(RSI):
                print("Calculating Indicators... waiting")
                time.sleep(5)
                continue


            buffer=SMA*buffer_percentage
            print(f" Price: {current_price:.5f} | SMA: {SMA:.5f} |  Buffer: {buffer:.5f}")

            if wallet.get('qty', 0) > 0:
                buy_price = wallet['buy_price']
                
                # Calculations sirf tab hongi jab share hoga
                sl_price = buy_price - (buy_price * STOP_LOSS_PERCENTAGE)
                target_price = buy_price + (buy_price * TARGET_PERCENTAGE)
                
                print(f"   Holding... Bought: {buy_price:.5f} |  SL: {sl_price:.5f} |  Target: {target_price:.5f}")

                # CONDITION 1: STOP LOSS HIT (Emergency Exit) 
                if current_price <= sl_price:
                        print(" STOP LOSS HIT! Selling immediately...")
                        wallet['balance'] = wallet['balance'] + (current_price * wallet['qty'])
                        log_trade("SELL", current_price, wallet['qty'], wallet['balance'], "Stop Loss Hit")
                        wallet['qty'] = 0
                        wallet['buy_price'] = 0.0
                        print(f"Sold at {current_price}. Loss Booked. New Balance: {wallet['balance']}")
                        save_data(wallet)


                
                # CONDITION 2: TARGET HIT (Profit Booking) 
                elif current_price >= target_price:
                        print(" TARGET HIT! Profit Booked...")
                        wallet['balance'] = wallet['balance'] + (current_price * wallet['qty'])
                        log_trade("SELL", current_price, wallet['qty'], wallet['balance'], "Target Hit")
                        wallet['qty'] = 0
                        wallet['buy_price'] = 0.0
                        print(f"Sold at {current_price}. Profit Booked. New Balance: {wallet['balance']}")
                        save_data(wallet)



                elif current_price < (SMA - buffer):
                    print("market is low ,SELL")
                    wallet['balance']=wallet['balance']+(current_price*(wallet['qty']))
                    log_trade("SELL", current_price, wallet['qty'], wallet['balance'], "SMA Strategy Exit")
                    wallet['qty']=0
                    print(f"Sold at {current_price}. New Balance: {wallet['balance']}")
                    save_data(wallet)

            
            else:
                if current_price > (SMA+buffer):
                    if RSI < RSI_OVERBOUGHT:  # Sirf tab khareedo jab RSI 70 se kam ho
                        print("🚀 BUY Signal Validated (RSI OK)")
                        if wallet['balance']>= current_price and wallet.get('qty',0)==0:
                            wallet['buy_price']=current_price
                            wallet['qty'] = 1
                            wallet['balance'] = wallet['balance'] - current_price

                            log_trade("BUY", current_price, wallet['qty'], wallet['balance'], "SMA+RSI Entry")
                            print(f"Bought at {current_price}. New Balance: {wallet['balance']}")
                            print(f" Price: {current_price:.2f} |  SMA: {SMA:.2f} |  Balance: {wallet['balance']}")
                            save_data(wallet)
                    else:
                        print(f" Signal Ignored! RSI is too high ({RSI:.2f}). Market Overbought.")

            wait_time=5
            print("waiting for 60 seconds ")
            time.sleep(60)


        except Exception as e:
            print(f"ERORR:---> {e}")
            time.sleep(wait_time)
            wait_time=wait_time*2
            
            

        
if __name__ == "__main__":
    my_bot()