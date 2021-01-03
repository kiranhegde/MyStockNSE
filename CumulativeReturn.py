import matplotlib.pyplot as plt
import pandas_datareader.data as web
import pandas as pd
import datetime
SymbolList=[]
# SymbolList=["IRCTC","BAJFINANCE","CIPLA","BHARTIARTL","HDFCBANK","ITC","LT","SUNPHARMA",'TATACONSUM',"TECHM"]
# SymbolList=["COROMANDEL","KOPRAN","AVANTIFEED","STRTECH","YESBANK","BSOFT","MASTEK"]
# SymbolList=["MIDHANI","GAIL","SBIN","MARKSANS","IOLCP","KSCL","DBL","STAR","DAAWAT","INDIGRID-IV"]
# SymbolList=["STAR","COROMANDEL","INSECTICID","NEULANDLAB","UPL","MARKSANS","IOLCP"]
# SymbolList=["STAR","COROMANDEL","INSECTICID","NEULANDLAB","IOLCP"]
# SymbolList=["HAL","BEML","BDL","MOIL","BHARATFORG"]
# SymbolList=['POWERGRID.NS','HAL.NS','WHIRLPOOL.NS','DMART.NS','SBILIFE.NS','BRITANNIA.NS','TATACONSUM.NS','IOLCP.NS','HDFCBANK.NS','TECHM.NS','BHARTIARTL.NS',"SUNPHARMA.NS","COROMANDEL.NS","MCX.NS",'ADANIGREEN.NS','LAURUSLABS.NS','CIPLA.NS',"ITC.NS",'RELIANCE.NS','STAR.NS']
# Kotak Only
# SymbolList=['ASIANPAINT.NS','LUPIN.NS','MARICO.NS','DABUR.NS','POWERGRID.NS','DMART.NS','BRITANNIA.NS','TATACONSUM.NS','IOLCP.NS','HDFCBANK.NS','TECHM.NS','BHARTIARTL.NS',"SUNPHARMA.NS","COROMANDEL.NS","MCX.NS",'ADANIGREEN.NS','LAURUSLABS.NS','CIPLA.NS',"ITC.NS",'RELIANCE.NS','STAR.NS']
# SymbolList=['BERGEPAINT.NS','CROMPTON.NS','ASIANPAINT.NS','LUPIN.NS','MARICO.NS','DABUR.NS','POWERGRID.NS','DMART.NS','BRITANNIA.NS','TATACONSUM.NS','IOLCP.NS','HDFCBANK.NS','TECHM.NS','BHARTIARTL.NS',"SUNPHARMA.NS","COROMANDEL.NS","MCX.NS",'ADANIGREEN.NS','LAURUSLABS.NS','CIPLA.NS',"ITC.NS",'RELIANCE.NS','STAR.NS']
# SymbolList=["ITC.NS",'UPL.NS','HDFCBANK.NS']
# SymbolList=["ITC.NS",'RELIANCE.NS','HDFCBANK.NS','SBIN.NS','ADANIENT.NS','ADANIGAS.NS','LT.NS','L&TFH.NS','HINDALCO.NS','TATASTEEL.NS','IRCTC.NS','DMART.NS','SBICARD.NS','IDEA.NS','INFY.NS']

# SymbolList=['HINDUNILVR.NS', 'DMART.NS','SEQUENT.NS','OFSS.NS', 'BERGEPAINT.NS', 'CIPLA.NS', 'COROMANDEL.NS', 'CROMPTON.NS', 'DMART.NS', 'HDFCBANK.NS', 'HINDUNILVR.NS', 'IRCTC.NS', 'ITC.NS', 'LUPIN.NS', 'MCX.NS', 'MINDTREE.NS', 'POWERGRID.NS', 'SBICARD.NS', 'SYNGENE.NS', 'TANLA.NS', 'WIPRO.NS']
SymbolList=["NEULANDLAB.NS"]

# sortedDict=dict(sorted(SymbolList.items()))
# SymbolList=sortedDict

start=pd.to_datetime('2010-01-01')
# end=datetime.datetime(2020,9,14)

for symb in SymbolList:
    # Symbol = symb+".NS"
    Symbol = symb

    stock= web.DataReader(Symbol, 'yahoo', start)
    stock.sort_index(inplace=True)
    stock.dropna()
    print(stock.head())
    print(stock.tail())

    stock['returns']=(stock['Close']/stock['Close'].shift(1))-1
    stock['returns']=stock['Close'].pct_change(1)
    stock['cumul_returns']=(1+stock['returns']).cumprod()
    stock['cumul_returns'].plot(label=symb,figsize=(10,8))
    plt.grid()
    plt.legend()
    plt.show()