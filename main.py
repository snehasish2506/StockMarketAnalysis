import streamlit as st
import pandas as pd
import CandleBar
import StockMarket
import DeepAnalysis
import Volume

dataStock = pd.read_excel('nse_sensex.xlsx', sheet_name='nse_sensex')

st.sidebar.title("Navigation")
myChoice = st.sidebar.radio("Select from the below options", ['Stock analysis','High and Low value','Candle Bar','Volume'])
if myChoice == 'Stock analysis':
    StockMarket.app(dataStock)
elif myChoice == 'High and Low value':
    DeepAnalysis.app(dataStock)
elif myChoice=='Candle Bar':
    CandleBar.app(dataStock)
elif myChoice=='Volume':
    Volume.app(dataStock)
