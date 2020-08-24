from tradingview_ta import TA_Handler

handler = TA_Handler()
handler.symbol = "COROMANDEL"
handler.interval = "1d" # 15 Minutes (1m,1h,1d,1W,1M)
handler.exchange = "NSE"
handler.screener = "india"


# Analysis
# There are 3 types of analysis in TradingView. Oscillators, moving averages, and summary (which is oscillators and moving averages combined).

analysis = handler.get_analysis()
print(analysis.summary)
# print(analysis.oscillators)
# print(analysis.moving_averages)
#Example output: {"RECOMMENDATION": "BUY", "BUY": 8, "NEUTRAL": 6, "SELL": 3}

# print(analysis.indicators)
# https://python-tradingview-ta.readthedocs.io/en/latest/how_it_works.html

print(analysis.time,analysis.symbol,analysis.exchange,analysis.screener)