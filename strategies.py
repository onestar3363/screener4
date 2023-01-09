import streamlit as st
import pandas as pd
import sqlalchemy
import ta
import numpy as np
import sqlalchemy
import time
import pandas_ta as pa
import os
import plotly
import plotly.graph_objs as go 
import graph
import dataframes

engine=sqlalchemy.create_engine('sqlite:///günlük.db')

names= dataframes.get_names()
framelist=dataframes.get_framelist()
framelistw=dataframes.get_framelistw()


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



def strategy(adx_value,adx_value2,h1,option1,option2,option3,sira):
    for name, frame, framew in zip(names,framelist, framelistw): 
        try:
            if  len(frame)>30 and len(framew)>30 and frame['ADX'].iloc[-1]>=adx_value and frame['ADX'].iloc[-1]<=adx_value2:
                
                if option1 == 'Buy' and (framew['Close'].iloc[-1]>framew['sup2'].iloc[-1] or framew['Close'].iloc[-1]>framew['sup4'].iloc[-1] or framew['Close'].iloc[-1]>framew['sup6'].iloc[-1] )\
                and (framew['Dec_EMA50'].iloc[-1]=='Buy' or framew['Dec_EMA20'].iloc[-1]=='Buy'):
                #and (framew['Consolidating2'].iloc[-h1]=='Yes' and framew['Consolidating3'].iloc[-h1]=='Yes'): 
                #and (framew['Trend MACD'].iloc[-1]=='Buy' and (framew['Dec_EMA50'].iloc[-1]=='Buy'or framew['Dec_EMA20'].iloc[-1]=='Buy'\
                #or framew['Close'].iloc[-1]>framew['sup2'].iloc[-1] or framew['Close'].iloc[-1]>framew['sup4'].iloc[-1])):
               
                    if option2 == 'breakout':
                       if (frame['Decision Super2'].iloc[-h1]=='Buy' or frame['Decision Super2'].iloc[-h1]=='Buy' or frame['Decision Super3'].iloc[-h1]=='Buy'\
                       or frame['EMA50_cross'].iloc[-h1]=='Buy' or frame['EMA50_cross'].iloc[-h1]=='Buy')\
                       and (frame['Close'].iloc[-h1]>frame['sup4'].iloc[-h1] or frame['Close'].iloc[-h1]>frame['sup6'].iloc[-h1]):
                                sira +=1
                                expander('breakout')
                                
                    if option2 == 'pullback':  
                       if (frame['Decision Super2'].iloc[-h1]=='Buy2' or frame['Decision Super2'].iloc[-h1]=='Buy2' or frame['Decision Super3'].iloc[-h1]=='Buy2'\
                       or frame['EMA50_cross'].iloc[-h1]=='Buy2' or frame['EMA50_cross'].iloc[-h1]=='Buy2' or frame['EMA200_cross'].iloc[-h1]=='Buy2')\
                       and (frame['Close'].iloc[-h1]>frame['sup4'].iloc[-h1] or frame['Close'].iloc[-h1]>frame['sup6'].iloc[-h1]):
                                sira +=1
                                expander()
                                
                    if option2 == 'consolidating':             
                       if (frame['Consolidating'].iloc[-h1]=='Yes' and frame['Consolidating2'].iloc[-h1]=='Yes' and frame['Consolidating3'].iloc[-h1]=='Yes')\
                       and (frame['Dec_EMA50'].iloc[-h1]=='Buy'and frame['Dec_EMA20'].iloc[-h1]=='Buy')\
                       and (frame['Close'].iloc[-h1]>frame['sup2'].iloc[-h1]>frame['sup4'].iloc[-h1]>frame['sup6'].iloc[-h1])\
                       and frame['Dec_EMA200'].iloc[-h1]=='Buy'\
                       and frame['Dec_MACD'].iloc[-h1]=='Buy':
                                sira +=1
                                expander() 
                    if option2 == 'week': 
                       if (framew['Decision Super2'].iloc[-2]=='Buy' or framew['Decision Super3'].iloc[-2]=='Buy')\
                       and (framew['Close'].iloc[-h1]>frame['sup4'].iloc[-h1] or framew['Close'].iloc[-h1]>framew['sup6'].iloc[-h1]):
                                sira +=1
                                expander('week breakout')   
                       elif (framew['Decision Super2'].iloc[-2]=='Buy2' or framew['Decision Super3'].iloc[-2]=='Buy2')\
                       and (framew['Close'].iloc[-h1]>frame['sup4'].iloc[-h1] or framew['Close'].iloc[-h1]>framew['sup6'].iloc[-h1]):
                                sira +=1
                                expander('week pullback')                                                         
                       #elif (frame['Close'].iloc[-h1]>frame['sup2'].iloc[-h1]>frame['sup4'].iloc[-h1] >frame['sup6'].iloc[-h1])\
                       #and (frame['Dec_EMA50'].iloc[-h1]=='Buy' or frame['Dec_EMA20'].iloc[-h1]=='Buy')\
                       #and frame['Close'].iloc[-h1]>frame['Close'].iloc[-h1-1]\
                       #and frame['Dec_MACD'].iloc[-h1]=='Buy'\
                       #and frame['Dec_EMA200'].iloc[-h1]=='Buy':
                       ##and frame['Close'].iloc[-h1]>frame['sup2'].iloc[-h1]>frame['sup4'].iloc[-h1]>frame['sup6'].iloc[-h1]:
                       ##and frame['ADX'].iloc[-h1]>frame['ADX'].iloc[-(h1+1)]:
                       ##and frame['Close'].iloc[-h]>frame['sup2'].iloc[-h]>frame['sup4'].iloc[-h]>frame['sup6'].iloc[-h]\
                       ##and frame['Decision ADX'].iloc[-h]=='Buy':                    
                       #         sira +=1
                       #         expander('cosku')                          
                if option1 == 'Sell' and (framew['Close'].iloc[-1]<framew['sup2'].iloc[-1] or framew['Close'].iloc[-1]<framew['sup4'].iloc[-1] or framew['Close'].iloc[-1]<framew['sup6'].iloc[-1])\
                and (framew['Dec_EMA20'].iloc[-1]=='Sell' or framew['Dec_EMA50'].iloc[-1]=='Sell'):
                #and (framew['Consolidating2'].iloc[-h1]=='Yes' and framew['Consolidating3'].iloc[-h1]=='Yes'):
                #(framew['Dec_EMA50'].iloc[-1]=='Sell'or framew['Dec_EMA20'].iloc[-1]=='Sell'\
                #or framew['Close'].iloc[-1]<framew['sup2'].iloc[-1] or framew['Close'].iloc[-1]<framew['sup4'].iloc[-1] or framew['Dec_MACD'].iloc[-1]=='Sell')):
                #(framew['Dec_EMA50'].iloc[-1]=='Sell'):
                #(framew['Trend MACD'].iloc[-1]=='Sell' or framew['Dec_EMA50'].iloc[-1]=='Sell'):
                    if option2 == 'breakout':
                       if (frame['Decision Super2'].iloc[-h1]=='Sell' or frame['Decision Super2'].iloc[-h1]=='Sell' or frame['Decision Super3'].iloc[-h1]=='Sell'\
                       or frame['EMA50_cross'].iloc[-h1]=='Sell' or frame['EMA20_cross'].iloc[-h1]=='Sell')\
                       and (frame['Close'].iloc[-h1]<frame['sup4'].iloc[-h1] or frame['Close'].iloc[-h1]<frame['sup6'].iloc[-h1]):
                                 sira +=1
                                 expander('breakout')
                    if option2=='pullback':
                       if (frame['Decision Super2'].iloc[-h1]=='Sell2' or frame['Decision Super2'].iloc[-h1]=='Sell2' or frame['Decision Super3'].iloc[-h1]=='Sell2'\
                       or frame['EMA50_cross'].iloc[-h1]=='Sell2' or frame['EMA50_cross'].iloc[-h1]=='Sell2' or frame['EMA200_cross'].iloc[-h1]=='Sell2')\
                       and (frame['Close'].iloc[-h1]<frame['sup4'].iloc[-h1] or frame['Close'].iloc[-h1]<frame['sup6'].iloc[-h1]):
                                sira +=1
                                expander('pullback')
                    if option2 == 'week':
                       if (framew['Decision Super2'].iloc[-2]=='Sell' or framew['Decision Super3'].iloc[-2]=='Sell')\
                       and (framew['Close'].iloc[-h1]<frame['sup4'].iloc[-h1] or framew['Close'].iloc[-h1]<framew['sup6'].iloc[-h1]):
                                sira +=1
                                expander('week breakout')
                       elif (framew['Decision Super2'].iloc[-2]=='Sell2' or framew['Decision Super3'].iloc[-2]=='Sell2')\
                       and (framew['Close'].iloc[-h1]<frame['sup4'].iloc[-h1] or framew['Close'].iloc[-h1]<framew['sup6'].iloc[-h1]):
                                sira +=1
                                expander('week pullback')
                    if option2=='consolidating':
                       if (frame['Consolidating2'].iloc[-h1]=='Yes' or frame['Consolidating3'].iloc[-h1]=='Yes')\
                       and frame['Dec_MACD'].iloc[-h1]=='Sell'\
                       and frame['Dec_EMA200'].iloc[-1]=='Sell':
                       #and frame['ADX'].iloc[-1]<frame['ADX'].iloc[-2]\
                       #and frame['Decision ADX'].iloc[-h]=='Buy':
                       #and frame['Dec_EMA50'].iloc[-1]=='Sell'
                               sira +=1
                               expander('consolidating')                         
            if option2 == 'Index' and name in indices:
                    sira +=1
                    expander()
            if name in option3:
                    sira +=1
                    expander('entered ticker')
        except Exception as e:
            st.write(name,e) 
        

    
