import streamlit as st
import pandas as pd
import sqlalchemy
import ta
import numpy as np
import yfinance as yf
import sqlalchemy
import time
import pandas_ta as pa
import os
import plotly
import plotly.graph_objs as go 
import base64
import dataframes
import strategies


@st.cache(suppress_st_warning=True)
def app():

    st.title('Screener')
    dataframes.getdata()
    start = time.perf_counter()
    #framelist=dataframes.get_framelist()
    #framelistw=dataframes.get_framelistw()
    end = time.perf_counter()
    st.write(end - start)
    
    sira=0
    option1 = st.sidebar.selectbox("Buy or Sell",('Buy','Sell')) 
    option2 = st.sidebar.selectbox("Which Indicator?", ('breakout','pullback','consolidating','week','EMASUPER','Index','EMA50','Supertrend','EMA20','MACD','ADX','EMA200'))
    adx_value= st.sidebar.number_input('ADX Value',min_value=10,value=18)
    adx_value2= st.sidebar.number_input('ADX Value_ust',min_value=10,value=60)
    h=st.sidebar.number_input('Geçmiş',value=1)
    h1=int(h)
    riskvalue=st.sidebar.number_input('Risk',min_value=1,value=1000)
    option3=st.sidebar.text_input('Ticker','')
    fark=st.sidebar.number_input('Fark',min_value=1.0,value=5.0,step=0.5)
    st.header(option1 + option2)
    indices=['US500/USD_S&P 500_INDEX_US','EU50/EUR_Euro Stoxx 50_INDEX_DE','^N225','XU030.IS']
    strategies.strategy(adx_value,adx_value2,h1,option1,option2,option3,sira)
if __name__ == "__main__":
    app()
