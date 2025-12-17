import yfinance as yf #as yf kyun likha? -> Taaki humein baar-baar pura naam yfinance na likhna pade. Humne uska nick-name rakh diya yf. Ab hum usse yf bulaayenge.
import pandas as pd 
'''Step 2: Ticker (Pehchan Patra / ID Card)
Ab Toolbox khul gaya. Par Python ko sapna thodi aayega ki tujhe Reliance ka data chahiye ya Tata ka? Humein Python ko batana padega ki Bhai, specifically TATA MOTORS ki file nikaal. '''
tata = yf.Ticker("TATAMOTORS.NS")
'''Note: .NS lagana zaroori hai kyunki hum NSE (National Stock Exchange) ka data maang rahe hain. Agar .NS nahi lagayega toh Yahoo confuse ho jayega ki ye America ki company hai kya.'''
'''
Step 3: .history() (Report Card Maangna)
Ab tere haath mein Tata Motors ki file (tata) aa gayi hai. Ab tu us file se Price nikalega. Price nikalne ke liye hum bolte hain: "History dikhao".
'''
data = tata.history(period="5d")