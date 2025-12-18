
as yf kyun likha? -> Taaki humein baar-baar pura naam yfinance na likhna pade. Humne uska nick-name rakh diya yf. Ab hum usse yf bulaayenge.
Step 2: Ticker (Pehchan Patra / ID Card)
Ab Toolbox khul gaya. Par Python ko sapna thodi aayega ki tujhe Reliance ka data chahiye ya Tata ka? Humein Python ko batana padega ki Bhai, specifically TATA MOTORS ki file nikaal. 
'''
Step 3: .history() (Report Card Maangna)
Ab tere haath mein Tata Motors ki file (tata) aa gayi hai. Ab tu us file se Price nikalega. Price nikalne ke liye hum bolte hain: "History dikhao".
'''
'''
data['Close']: Humne puri table mein se sirf 'Close' price wali line uthayi.

.iloc: Humne kaha "Mujhe specific location par jana hai."

[-1]: Humne kaha "Last wala de." (Agar -2 likhte toh kal ka milta, -3 likhte toh parso ka).
'''

 current_price=data['Close'].iloc[-1] #ye current price nikalega 
 current_price_sma5=data['SMA_5'].iloc[-1] #ye last 5 days ka moving average nikalega 
 time.sleep(60)#ye code execution ko pause karega 60 seconds ke liye

 