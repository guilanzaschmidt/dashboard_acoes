import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.express as px
import pytz as pt
from datetime import datetime as dt
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_extras.grid import grid

def build_sidebar():
    st.image("Images/logo-250-100-transparente.png")
    ticket_list = pd.read_csv("tickers_ibra.csv", index_col=0)
    tickers = st.multiselect(label="Selecione a ação",options=ticket_list, placeholder="Código Ação")
    tickers = [t+".SA" for t in tickers]
    #start_date = tz.localize(dt(2024,1,1))
    #end_date = tz.localize(dt.today())
    start_date = st.date_input("De", format="DD/MM/YYYY",value=dt(2024,1,2))
    end_date = st.date_input("Até", format="DD/MM/YYYY",value="today")

    if tickers:
        prices = yf.download(tickers, start = start_date, end = end_date, auto_adjust=True)["Close"]
        prices.columns = prices.columns.str.rstrip(".SA")
        return tickers, prices
    return None, None

def build_main(tickers, prices):
    weigths = np.ones(len(tickers))/len(tickers)
    prices['portfolio'] = prices @ weigths
    norm_prices = 100 * prices / prices.iloc[0]
    returns = prices.pct_change()[1:]
    vols = returns.std()*np.sqrt(252)
    rets = (norm_prices.iloc[-1] - 100) / 100

    mygrid = grid(5 ,5 , 5 ,5 ,5 ,5, vertical_align="top")
    for t in prices.columns:
        c = mygrid.container(border=True)
        c.subheader(t, divider="red")
        colA, colB, colC, = c.columns(3)
        if t == "portfolio":
            colA.image("Images/pie-chart-dollar-svgrepo-com.svg")   
        else:     
            colA.image(f'https://raw.githubusercontent.com/thefintz/icones-b3/main/icones/{t}.png', width=85)    
        colB.metric(label="retorno", value=f"{rets[t]:.0%}")
        colC.metric(label="volatidade", value=f"{vols[t]:.0%}")
        style_metric_cards(background_color='rgba(255,255,255,0)')

    col1, col2 = st.columns(2, gap='large')
    with col1:
        st.subheader("Desempenho Relativo")
        st.line_chart(norm_prices, height=600)

    with col2:
        st.subheader("RiscoxRetorno")
        fig = px.scatter(
            x=vols,
            y=rets,
            color=rets/vols,
            color_continuous_scale=px.colors.sequential.Bluered_r
        )       
    #st.dataframe(prices)

st.set_page_config(layout="wide")    

with st.sidebar:
    tickers, prices = build_sidebar()

if tickers:
    build_main(tickers, prices)
st.title("Analise ações brasileiras")