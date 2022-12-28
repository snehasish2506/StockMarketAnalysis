import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
from datetime import datetime
from dateutil.relativedelta import relativedelta

def GetShareDetails(shareName, rangeType, dataStock, yearWise, monthWise):
    dataStock['DateYear'] = pd.DatetimeIndex(dataStock['DATE']).year
    dataStock['TempMonth'] = 'January'
    dataStock['YearDate'] = dataStock['TempMonth'].astype(str) + ", " + dataStock['DateYear'].astype(str)
    dataStock['YearDate'] = pd.to_datetime(dataStock.YearDate)
    dataStock['DateMonth'] = pd.DatetimeIndex(dataStock['DATE']).month_name()
    dataStock['MonthYear'] = dataStock.DateMonth.astype(str) + ", " + dataStock.DateYear.astype(str)
    dataStock['YearMonth'] = pd.to_datetime(dataStock.MonthYear)

    if monthWise:
        dataMonthYearwiseHighValueSum = pd.DataFrame(
        dataStock.groupby(['YearMonth', 'MonthYear', 'SYMBOL'])[rangeType].sum().reset_index())
        filterdata = dataMonthYearwiseHighValueSum.loc[(dataMonthYearwiseHighValueSum.SYMBOL == shareName), :]
        fig = go.Figure(data=[go.Candlestick(x=filterdata['YearMonth'],
                                             open=filterdata['OPEN'],
                                             high=filterdata['HIGH'],
                                             low=filterdata['LOW'],
                                             close=filterdata['CLOSE'])])

        fig.update_xaxes(rangeslider_visible=True,
                         rangeselector=dict(
                           buttons=list([
                             dict(count=1, label="1 month", step="month", stepmode="backward"),
                             dict(count=6, label="6 months", step="month", stepmode="backward"),
                             dict(count=1, label="1 year", step="year", stepmode="backward"),
                             dict(count=3, label="3 years", step="year", stepmode="backward"),
                             dict(step="all")
                           ])
                         ))
        # st.plotly_chart(fig)

    if yearWise:
        dataYearwiseHighValueSum = pd.DataFrame(
        dataStock.groupby(['YearDate', 'DateYear', 'SYMBOL'])[rangeType].sum().reset_index())
        filterdata = dataYearwiseHighValueSum.loc[(dataYearwiseHighValueSum.SYMBOL == shareName), :]
        fig = go.Figure(data=[go.Candlestick(x=filterdata['YearDate'],
                                             open=filterdata['OPEN'],
                                             high=filterdata['HIGH'],
                                             low=filterdata['LOW'],
                                             close=filterdata['CLOSE'])])

        fig.update_xaxes(rangeslider_visible=True,
                         rangeselector=dict(
                           buttons=list([
                             dict(count=1, label="1 year", step="year", stepmode="backward"),
                             dict(count=2, label="2 year", step="year", stepmode="backward"),
                             dict(count=3, label="3 year", step="year", stepmode="todate"),
                             dict(count=4, label="4 year", step="year", stepmode="backward"),
                             dict(step="all")
                           ])
                         ))
        # st.plotly_chart(fig)
    return fig



def app(dataStock):
    shareName = st.selectbox("Select Share", dataStock.SYMBOL.unique())
    duration = st.selectbox("Select duration", ['Days', 'Month', 'Year'])

    if duration == 'Month':
        monthWise = True
        yearWise = False
        sharePrice = ['OPEN', 'HIGH', 'LOW', 'CLOSE','VWAP']
        st.write("This is candle bar")
        fig = GetShareDetails(shareName, sharePrice, dataStock, yearWise, monthWise)

    elif duration =='Days':
        filterdata = dataStock.loc[dataStock.SYMBOL == shareName, :]
        filterdata['MA5'] = filterdata.CLOSE.rolling(5).mean()
        filterdata['MA20'] = filterdata.CLOSE.rolling(20).mean()

        st.write("This is candle bar")
        fig = go.Figure(data=[go.Candlestick(x=filterdata['DATE'],
                                             open=filterdata['OPEN'],
                                             high=filterdata['HIGH'],
                                             low=filterdata['LOW'],
                                             close=filterdata['CLOSE'],  name ='Candle'),
                              go.Scatter(x=filterdata.DATE, y=filterdata.MA5, name ='MA5', line=dict(color='blue', width=1)),
                              go.Scatter(x=filterdata.DATE, y=filterdata.MA20,  name ='MA20', line=dict(color='green', width=1)),
                              go.Scatter(x=filterdata.DATE, y=filterdata.VWAP,name='VWAP', line=dict(color='red', width = 1))
                              ])
        # st.plotly_chart(fig)

        fig.update_xaxes(rangeslider_visible=True,
                         rangeselector=dict(
                             buttons=list([
                                 dict(count=7, label="1 week", step="day", stepmode="backward"),
                                 dict(count=1, label="1 month", step="month", stepmode="backward"),
                                 dict(count=6, label="6 months", step="month", stepmode="backward"),
                                 dict(count=1, label="1 year", step="year", stepmode="backward"),
                                 dict(step="all")
                             ])
                         ))

        fig.update_layout(width=1000, height=500)
    else:
        yearWise = True
        monthWise = False
        sharePrice = ['OPEN', 'HIGH', 'LOW', 'CLOSE']
        st.write("This is candle bar")
        fig = GetShareDetails(shareName, sharePrice, dataStock, yearWise, monthWise)

    st.plotly_chart(fig)
