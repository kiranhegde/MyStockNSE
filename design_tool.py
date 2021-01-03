from tradingview_ta import TA_Handler

handler = TA_Handler()
handler.symbol = "COROMANDEL"
handler.interval = "1d" # 15 Minutes (1m,1h,1d,1W,1M)
handler.exchange = "NSE"
handler.screener = "india"


# Analysis
# There are 3 types of analysis in TradingView. Oscillators, moving averages, and summary (which is oscillators and moving averages combined).

analysis = handler.get_analysis()
# print(analysis.summary)
# print(analysis.oscillators)
# print(analysis.moving_averages)
#Example output: {"RECOMMENDATION": "BUY", "BUY": 8, "NEUTRAL": 6, "SELL": 3}

# print(analysis.indicators)
# https://python-tradingview-ta.readthedocs.io/en/latest/how_it_works.html

# print(analysis.time,analysis.symbol,analysis.exchange,analysis.screener)

import pandas as pd
import sqlite3

db_file = "MyInvestment.db"

# Read sqlite query results into a pandas DataFrame
con = sqlite3.connect(db_file)
df = pd.read_sql_query("SELECT * from sale", con)
con.close()
# ['id', 'agency', 'exchange', 'equity', 'buy_date', 'buy_price', 'trade_date', 'settle_date', 'trade_price', 'quantity', 'brokerage', 'gst', 'stt', 'itax', 'remarks']
print(list(df.columns))

# Verify that result of SQL query is stored in the dataframe
# print(df.values)
# for val in df.values:
#     print( list(val))

