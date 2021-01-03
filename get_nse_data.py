
def get_latest_price(Symbol):
    import pandas_datareader.data  as web
    import datetime

    LastPrice = web.get_data_yahoo(Symbol)
    # print(LastPrice.tail(2))
    # print(list(LastPrice))
    # exit()
    LastPrice = LastPrice.at[LastPrice.index[-1], 'Adj Close']

    return round(LastPrice, 2)
#
# Symbol="KOPRAN.NS"
# CurrentPrice=get_latest_price(Symbol)
# print(CurrentPrice)


def download_data_for_month(Symbol,delta):
    from nsepy import get_history as gh
    from datetime import date, timedelta
    import pandas as pd

    # try:
    Symbol.replace('&','%26')
    # print(Symbol)
    end_day = date.today()
    start_day = end_day - timedelta(delta)
    stock_price_df = gh(symbol=Symbol, start=start_day, end= end_day)
    data = pd.DataFrame(stock_price_df, columns=['Symbol', 'Open', 'Close', 'Last'])
    currentPrice = list(data.Close)[0]
    # header = list(data)
    # print(currentPrice)
    #
    # except:
    #     currentPrice=0.0

    return currentPrice

# delta=0
# Symbol="STAR "
# Symbol.replace('&','%26')
# print(Symbol)
# CurrentPrice=download_data_for_month(Symbol,delta)
# print(CurrentPrice)

# print(df)
# print("----------")
# for index,row in df.iterrows():
#     print(row)


def get_recommendation(symbol,delta):
    from tradingview_ta import TA_Handler

    handler = TA_Handler()
    handler.symbol = symbol
    handler.interval = delta # 15 Minutes (1m,1h,1d,1W,1M)
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
    return analysis.summary

#
# units = {"Minute": "m", "Hour": "h", "Day": "d", "Week": "W", "Month": "M"}
#
# symbol="bsoft"
# delta="1D"
# print("*",symbol,delta)
#
#
# reco = get_recommendation(symbol, delta)
# print(reco)