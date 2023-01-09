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
import getdata1

if __name__ == '__main__':

    st.set_page_config(layout="wide")
    st.title('Screener')
    getdata1.getdata()
    connection_url='sqlite:///günlük.db'
    connection_url2='sqlite:///haftalik.db'
    engine= connect_engine(connection_url) 
    enginew= connect_enginew(connection_url2)
    start = time.perf_counter()
    names=get_names()
    framelist=get_framelist()
    framelistw=get_framelistw()
    end = time.perf_counter()
    st.write(end - start)
    
    
    
