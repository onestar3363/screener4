import streamlit as st
import pandas as pd
import sqlalchemy
import numpy as np
import yfinance as yf
import sqlalchemy
import time
import os
import base64

if __name__ == '__main__':
    start = time.perf_counter()
    @st.cache(suppress_st_warning=True)
    def getdata():
        if os.path.exists("günlük.db"):
            os.remove("günlük.db")
        elif os.path.exists("haftalik.db"):
            os.remove("haftalik.db")
        index = 0
        engine=sqlalchemy.create_engine('sqlite:///günlük.db')
        enginew=sqlalchemy.create_engine('sqlite:///haftalik.db')
        with st.empty():
            index += 1
            bsymbols1=pd.read_csv('hepsi.csv',header=None)
            bsymbols=bsymbols1.iloc[:,0].to_list()
            bnameslist = bsymbols1.iloc[:,1].to_list()
            for bticker, bnames in zip (bsymbols,bnameslist):
                st.write(f"⏳ {index,bticker} downloaded")
                index += 1
                df=yf.download(bticker,period="1y",interval='1d',auto_adjust=True )
                ohlcv_dict = {'Open': 'first',
                  'High': 'max',
                  'Low': 'min',
                  'Close': 'last',
                  'Volume': 'sum'
                 }
                df.to_sql(bnames,engine, if_exists='replace')
                df2w = df.resample('W-FRI').agg(ohlcv_dict)
                df2w.dropna(inplace=True)
                df2w.to_sql(bnames,enginew, if_exists='replace')
            now=pd.Timestamp.now().strftime("%d-%m-%Y, %H:%M")
            st.write('Last downloaded', index,bticker,now)
            return(index,bticker,now)
    lastindex=getdata()
    end = time.perf_counter() 
    st.write('Last downloaded', lastindex, 'Süre', end - sta
