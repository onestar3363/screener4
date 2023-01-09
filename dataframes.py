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
import strategies
import graph


st.set_page_config(layout="wide")
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
        for bticker, bnames in zip (bsymbols[:5],bnameslist[:5]):
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

def MACDdecision(df):
    df['MACD_diff']= ta.trend.macd_diff(df.Close)
    df['MACD']= ta.trend.macd(df.Close)
    df['MACD_signal']=ta.trend.macd_signal(df.Close)
    #df.loc[(df.MACD_diff>0) & (df.MACD_diff.shift(1)<0),'Dec_MACD']='Buy'
    #df.loc[(df.MACD_diff<0) & (df.MACD_diff.shift(1)>0),'Dec_MACD']='Sell'
    df.loc[(df.MACD_diff>0),'Dec_MACD']='Buy'
    df.loc[(df.MACD_diff<0),'Dec_MACD']='Sell'
    df.loc[(df.MACD_diff.shift(1)<df.MACD_diff),'Trend MACD']='Buy'
    df.loc[(df.MACD_diff.shift(1)>df.MACD_diff),'Trend MACD']='Sell'

def EMA_decision(df):

    df['EMA20'] = ta.trend.ema_indicator(df.Close,window=20)
    df.loc[(df.Close>df['EMA20']), 'Dec_EMA20'] = 'Buy'
    df.loc[(df.Close<df['EMA20']), 'Dec_EMA20'] = 'Sell'
    df.loc[((df.Close>=df.EMA20)& (df.Close.shift(1)<=df.EMA20.shift(1))), 'EMA20_cross'] = 'Buy'
    df.loc[(df.Close.shift(1)>=df.EMA20.shift(1))&(df.Low<=df.EMA20), 'EMA20_cross'] = 'Buy2'
    df.loc[(df.Close.shift(1)<=df.EMA20.shift(1))&(df.High>=df.EMA20)&(df.Close<=df.EMA20)&(df.Close.shift(1)<df.Close), 'EMA20_cross'] = 'Sell2' 
    df.loc[((df.Close<=df.EMA20)& (df.Close.shift(1)>=df.EMA20.shift(1))), 'EMA20_cross'] = 'Sell'


    df['EMA50'] = ta.trend.ema_indicator(df.Close,window=50)
    df.loc[(df.Close>df['EMA50']), 'Dec_EMA50'] = 'Buy'
    df.loc[(df.Close<df['EMA50']), 'Dec_EMA50'] = 'Sell'
    df.loc[((df.Close>=df.EMA50)& (df.Close.shift(1)<=df.EMA50.shift(1))), 'EMA50_cross'] = 'Buy'
    df.loc[(df.Close.shift(1)>=df.EMA50.shift(1))&(df.Low<=df.EMA50), 'EMA50_cross'] = 'Buy2'
    df.loc[(df.Close.shift(1)<=df.EMA50.shift(1))&(df.High>=df.EMA50)&(df.Close<=df.EMA50)&(df.Close.shift(1)<df.Close), 'EMA50_cross'] = 'Sell2' 
    df.loc[((df.Close<=df.EMA50)& (df.Close.shift(1)>=df.EMA50.shift(1))), 'EMA50_cross'] = 'Sell'


    df['EMA200'] = ta.trend.ema_indicator(df.Close,window=200)
    df.loc[(df.Close>df['EMA200']), 'Dec_EMA200'] = 'Buy'
    df.loc[(df.Close<df['EMA200']), 'Dec_EMA200'] = 'Sell'
    df.loc[((df.Close>=df.EMA200)& (df.Close.shift(1)<=df.EMA200.shift(1))), 'EMA200_cross'] = 'Buy'
    df.loc[((df.Close<=df.EMA200)& (df.Close.shift(1)>=df.EMA200.shift(1))), 'EMA200_cross'] = 'Sell'


def ADX_decision(df):
    df['ADX']= ta.trend.adx(df.High, df.Low, df.Close)
    #df['ADX']=pa.adx(high=df['High'],low=df['Low'],close=df['Close'],mamode='ema',append=True)['ADX_14']
    df['ADX_neg']=ta.trend.adx_neg(df.High, df.Low, df.Close,fillna=True)
    df['ADX_pos']=ta.trend.adx_pos(df.High, df.Low, df.Close,fillna=True)
    #df['DIOSQ']=df['ADX_pos']-df['ADX_neg']
    #df['DIOSQ_EMA']=ta.trend.ema_indicator(df.DIOSQ,window=10)
    df.loc[(df.ADX>df.ADX.shift(1)) ,'Decision ADX']='Buy'
    #df.loc[(df.DIOSQ>df.DIOSQ_EMA)& (df.DIOSQ.shift(1)<df.DIOSQ_EMA.shift(1)), 'Dec_DIOSQ'] = 'Buy'
    #df.loc[(df.DIOSQ<df.DIOSQ_EMA)& (df.DIOSQ.shift(1)>df.DIOSQ_EMA.shift(1)), 'Dec_DIOSQ'] = 'Sell'
    

def Supertrend(df):
    df['sup']=pa.supertrend(high=df['High'],low=df['Low'],close=df['Close'],length=10,multiplier=1.0)['SUPERTd_10_1.0']
    df['sup2']=pa.supertrend(high=df['High'],low=df['Low'],close=df['Close'],length=10,multiplier=1.0)['SUPERT_10_1.0']
    df['sup3']=pa.supertrend(high=df['High'],low=df['Low'],close=df['Close'],length=10,multiplier=2.0)['SUPERTd_10_2.0']
    df['sup4']=pa.supertrend(high=df['High'],low=df['Low'],close=df['Close'],length=10,multiplier=2.0)['SUPERT_10_2.0']
    df['sup5']=pa.supertrend(high=df['High'],low=df['Low'],close=df['Close'],length=10,multiplier=3.0)['SUPERTd_10_3.0']
    df['sup6']=pa.supertrend(high=df['High'],low=df['Low'],close=df['Close'],length=10,multiplier=3.0)['SUPERT_10_3.0']
    
    
    df.loc[(df.sup==1)&(df.sup.shift(1)==-1), 'Decision Super'] = 'Buy'
    df.loc[(df.Close.shift(1)>=df.sup2.shift(1))&(df.Low<=df.sup2), 'Decision Super'] = 'Buy2'    
    df.loc[(df.Close.shift(1)<=df.sup2.shift(1))&(df.High>=df.sup2), 'Decision Super'] = 'Sell2'
    df.loc[(df.sup==-1)&(df.sup.shift(1)==1), 'Decision Super'] = 'Sell' 

    
    
    df.loc[(df.sup3==1)&(df.sup3.shift(1)==-1), 'Decision Super2'] = 'Buy'
    df.loc[(df.Close.shift(1)>=df.sup4.shift(1))&(df.Low<=df.sup4), 'Decision Super2'] = 'Buy2'    
    df.loc[(df.Close.shift(1)<=df.sup4.shift(1))&(df.High>=df.sup4), 'Decision Super2'] = 'Sell2'
    df.loc[(df.sup3==-1)&(df.sup3.shift(1)==1), 'Decision Super2'] = 'Sell'

    
    df.loc[(df.sup5==1)&(df.sup5.shift(1)==-1), 'Decision Super3'] = 'Buy'
    df.loc[(df.Close.shift(1)>=df.sup6.shift(1))&(df.Low<=df.sup6), 'Decision Super3'] = 'Buy2'    
    df.loc[(df.Close.shift(1)<=df.sup6.shift(1))&(df.High>=df.sup6), 'Decision Super3'] = 'Sell2'
    df.loc[(df.sup5==-1)&(df.sup5.shift(1)==1), 'Decision Super3'] = 'Sell' 

    
    df.loc[(df.sup2 == df.sup2.shift(1)), 'Consolidating'] = 'Yes'
    df.loc[(df.sup4 == df.sup4.shift(1)), 'Consolidating2'] = 'Yes'
    df.loc[(df.sup6 == df.sup6.shift(1)), 'Consolidating3'] = 'Yes'
    
   
def ATR_decision(df):
    df['ATR']= ta.volatility.average_true_range(df.High, df.Low, df.Close,window=10)
    df['ATR%'] = df['ATR']/df.Close*100
    df['RISK']= 2*df['ATR']/701*100        

# def Stoch_decision(df):
#     df['Stoch'] = ta.momentum.stoch(df.High, df.Low, df.Close, smooth_window=3)
#     df['Stoch_Signal'] = ta.momentum.stoch_signal(df.High, df.Low, df.Close, smooth_window=3)
#     df.loc[(df.Stoch>df.Stoch_Signal)& (df.Stoch.shift(1)<df.Stoch_Signal.shift(1)) & (df.Stoch_Signal<20), 'Decision Stoch'] = 'Buy'  

def Stochrsi_decision(df):
     df['Stochrsi_d'] = ta.momentum.stochrsi_d(df.Close)
     df['Stochrsi_k'] = ta.momentum.stochrsi_k(df.Close)
     #df.loc[(df.Stochrsi_k.shift(1)>0.8)&(df.Stochrsi_k<0.8),'DecStoch']='Sell'
        

def Volume_decision(df):
    df['Volume_EMA']=ta.trend.ema_indicator(df.Volume,window=10)


@st.cache(allow_output_mutation=True)
def connect_engine(url):
    engine=sqlalchemy.create_engine(url) 
    return engine
@st.cache(allow_output_mutation=True)
def connect_enginew(url):
    enginew=sqlalchemy.create_engine(url) 
    return enginew

def get_names():
    names= pd.read_sql('SELECT name FROM sqlite_master WHERE type="table"',engine)
    names = names.name.to_list()
    return names
      
@st.cache(hash_funcs={sqlalchemy.engine.base.Engine:id},suppress_st_warning=True,max_entries=1)
def get_framelist():
    framelist=[]
    for name in names:
        framelist.append(pd.read_sql(f'SELECT Date,Close,Open,High,Low,Volume FROM "{name}"',engine))    
    np.seterr(divide='ignore', invalid='ignore')
    with st.empty():
        sira=0
        for name,frame in zip(names,framelist): 
            if len(frame)>30:
                MACDdecision(frame)
                EMA_decision(frame)
                ADX_decision(frame)
                Supertrend(frame)
                ATR_decision(frame)
                Volume_decision(frame)
                sira +=1
                st.write('günlük',sira,name)             
    return framelist    
@st.cache(hash_funcs={sqlalchemy.engine.base.Engine:id},suppress_st_warning=True,max_entries=1)      
def get_framelistw():
    framelistw=[]
    for name in names: 
        framelistw.append(pd.read_sql(f'SELECT Date,Close,Open,High,Low,Volume FROM "{name}"',enginew))   
    np.seterr(divide='ignore', invalid='ignore')
    with st.empty():
        sira=0
        for name,framew in zip(names,framelistw): 
            if  len(framew)>30 :
                MACDdecision(framew)
                EMA_decision(framew)
                ADX_decision(framew)
                Supertrend(framew)
                ATR_decision(framew)
                Volume_decision(framew)
                sira +=1
                st.write('haftalik',sira,name)              
    return framelistw
connection_url='sqlite:///günlük.db'
connection_url2='sqlite:///haftalik.db'
engine= connect_engine(connection_url) 
enginew= connect_enginew(connection_url2)
names=get_names()
framelist=get_framelist()
framelistw=get_framelistw()
