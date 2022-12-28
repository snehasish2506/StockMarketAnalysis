import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
# from urllib.parse import quote
from datetime import datetime
from dateutil.relativedelta import relativedelta


def app(dataStock):
    shareName = st.selectbox("Select Share", dataStock.SYMBOL.unique())
    filterdata = dataStock.loc[dataStock.SYMBOL == shareName,:]
    maxDate = filterdata.iloc[-1,0]
    endDate = datetime(int(str(maxDate).split(' ')[0].split('-')[0]),int(str(maxDate).split(' ')[0].split('-')[1]),int(str(maxDate).split(' ')[0].split('-')[2]))
    startDate = endDate - relativedelta(years=1)
    highValue = filterdata.loc[(filterdata.DATE >= startDate) & (filterdata.DATE <= endDate),['HIGH']].max().tolist()[0]
    lowValue = filterdata.loc[(filterdata.DATE >= startDate) & (filterdata.DATE<=endDate),['LOW']].min().tolist()[0]
    st.markdown("52 weeks high for " + shareName + " was " + "<font color = 'green'>" + str(highValue) + "</font>", unsafe_allow_html=True)
    st.markdown("52 weeks low for " + shareName + " was " + "<font color='red'>" + str(lowValue) + "</font>", unsafe_allow_html=True)