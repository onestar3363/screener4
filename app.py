import streamlit as st
import yfinance as yf
from PIL import Image
import requests
from io import BytesIO
import financial
import stockchart
import backtest


if __name__ == '__main__':

    st.title('Trading DashBoard')
    url = 'https://g.foolcdn.com/editorial/images/602904/why-tesla-stock-is-up-today.jpg'
    response = requests.get(url)
    img = Image.open(BytesIO(response. content))
