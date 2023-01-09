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
    start = time.perf_counter()
    getdata()
    lastindex=getdata1.getdata()
    end = time.perf_counter() 
    st.write('Last downloaded', lastindex, 'Süre', end - start)
    
    
    
