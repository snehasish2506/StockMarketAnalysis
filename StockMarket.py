import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
# from urllib.parse import quote


def GetShareDetails(shareName, rangeType, dataStock, yearWise, monthWise):

  dataStock['DateYear'] = pd.DatetimeIndex(dataStock['DATE']).year
  dataStock['TempMonth'] = 'January'
  dataStock['YearDate'] = dataStock['TempMonth'].astype(str) + ", " + dataStock['DateYear'].astype(str)
  dataStock['YearDate'] = pd.to_datetime(dataStock.YearDate)
  dataStock['DateMonth'] = pd.DatetimeIndex(dataStock['DATE']).month_name()
  # dataStock['MonthYear'] = dataStock['DateMonth'] + ", " + str(dataStock['DateYear'])
  dataStock['MonthYear'] = dataStock.DateMonth.astype(str) + ", " + dataStock.DateYear.astype(str)
  # dataStock['YearMonth'] = pd.to_datetime(dataStock.MonthYear).dt.year * 100 + pd.to_datetime(dataStock.MonthYear).dt.month
  dataStock['YearMonth'] = pd.to_datetime(dataStock.MonthYear)

  if monthWise:
    dataMonthYearwiseHighValueSum = pd.DataFrame(
      dataStock.groupby(['YearMonth', 'MonthYear', 'SYMBOL'])[rangeType].sum().reset_index())
    myVar = dataMonthYearwiseHighValueSum.loc[(dataMonthYearwiseHighValueSum.SYMBOL == shareName), :]
    fig = px.line(myVar, x="YearMonth", y=rangeType, custom_data=['MonthYear'],
                  title='Month wise Distribution of ' + shareName)
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
    st.plotly_chart(fig)

  if yearWise:
    dataYearwiseHighValueSum = pd.DataFrame(
      dataStock.groupby(['YearDate', 'DateYear', 'SYMBOL'])[rangeType].sum().reset_index())
    myVar = dataYearwiseHighValueSum.loc[(dataYearwiseHighValueSum.SYMBOL == shareName), :]
    fig = px.line(myVar, x="YearDate", y=rangeType, title='Year wise value distribution of ' + shareName)
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
    st.plotly_chart(fig)



def app(dataStock):
  with st.form("my_form"):
    shareName = st.selectbox("Select Share",dataStock.SYMBOL.unique() )
    sharePrice = st.selectbox("Select price type", ['OPEN','HIGH','LOW','LAST','CLOSE'])
    # duration = st.selectbox("Select duration",['1 month','3 months', '6 months', '1 year','5 years'])
    duration = st.selectbox("Select duration", ['Days', 'Month', 'Year'])
    submitted = st.form_submit_button("Submit")

  if duration=='Month':
    monthWise = True
    yearWise = False
  else:
    yearWise = True
    monthWise = False


  GetShareDetails(shareName, sharePrice, dataStock, yearWise, monthWise)
