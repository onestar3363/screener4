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


#def get_names():
#    names= pd.read_sql('SELECT name FROM sqlite_master WHERE type="table"',engine)
#    names = names.name.to_list()
#    return names

names= dataframes.get_names()
framelist=dataframes.get_framelist()
framelistw=dataframes.get_framelistw()





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
                                expander(option2)
                                
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
        
 def expander(option2,sira):
       with st.expander(option2+' '+str(sira) +') '+ name+'/'+' RISK= '+str(frame['RISK'].iloc[-1].round(2))+'/ %ATR='+str(frame['ATR%'].iloc[-1].round(2))+'/ %wATR='+str(framew['ATR%'].iloc[-1].round(2))):
           #st.write(str(sira) +') '+ name+'/'+' RISK= '+str(frame['RISK'].iloc[-1].round(2))+'/ %ATR='+str(frame['ATR%'].iloc[-1].round(2)))
           #col6, col3, col4 = st.columns([1, 1, 1])
           col3, col4 = st.columns([1, 1])
           col3.write(frame[['Close','ATR%','ADX','EMA20_cross','EMA50_cross','Decision Super','Decision Super2','Decision Super3','Dec_MACD','Trend MACD','MACD_diff']].tail(2))
           col4.write(framew[['Close','ATR%','ADX','EMA20_cross','EMA50_cross','Decision Super','Decision Super2','Decision Super3','Dec_MACD','Trend MACD','MACD_diff']].tail(2))
           #col6.write(frameh[['Close','ATR%','ADX','Dec_EMA50','Dec_MACD','Trend MACD','MACD_diff']].tail(2))
           #col5, col1, col2 = st.columns([1, 1, 1])
           col1, col2 = st.columns([1, 1])
           r=100
           fig=get_figures(frame,r)
           r=40
           figw=get_figures(framew,r)
           r=300      
           col1.plotly_chart(fig,use_container_width=True)
           col2.plotly_chart(figw,use_container_width=True)
    
