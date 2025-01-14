import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.express as px
import pytz as pt
from datetime import datetime as dt
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_extras.grid import grid

st.title("Analise ações brasileiras")

def build_sidebar():
    st.image("Images/logo-250-100-transparente.png")
    ticket_list = pd.read_csv("tickers_ibra.csv", index_col=0)
    tickers = st.multiselect(label="Selecione a ação",options=ticket_list, placeholder="Código Ação")
    tickers = [t+".SA" for t in tickers]
    #start_date = tz.localize(dt(2024,1,1))
    #end_date = tz.localize(dt.today())
    start_date = st.date_input("De", format="DD/MM/YYYY",value=dt(2024,1,2))
    end_date = st.date_input("Até", format="DD/MM/YYYY",value=dt(2025,1,13))

    if tickers:
        prices = yf.download(tickers, start = start_date, end = end_date, auto_adjust=True)["Close"]
        return tickers, prices

def build_main(tickers, prices):
    st.dataframe(prices)

with st.sidebar:
    tickers, prices = build_sidebar()

build_main(tickers, prices)