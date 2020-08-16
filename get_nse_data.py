from nsepy import get_history as gh
from datetime import date, timedelta
import pandas as pd

def download_data_for_month(Symbol,delta):

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
