"""
in a bash terminal:

cd /home/hiran/Finboard
streamlit run "./streamlit_app.py"

"""

import os
import streamlit as st
import plotly.express as px
import pandas as pd
# import pip
# print(pip.__version__)
import numpy as np
import yfinance as yf

# script_dir = os.path.dirname ( os.path.abspath(__file__) ) 
# os.chdir(script_dir)

############
st.title("Stock Market Dashboard (yfinance)")

st.write( "First, Let's take a single Security as a reference points")
############

ticker_list = pd.read_csv("YahooTickerSymbols_utf8.csv")
ticker = st.selectbox("Analyse this Company", options=ticker_list.Ticker, index=3)
# ticker = "NVDA"
period = st.selectbox("Go back this much", 
                      options=("1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"),
                      index=6)
# period = "1y"

# Create Dataframe
data = yf.Ticker(ticker)
data10y = data.history(period=period)
data10y["Day_Avg"] = (data10y["Open"] + data10y["Close"])/2
data10y["Rolling_20"] = data10y["Day_Avg"].rolling(window = 20, min_periods=1).mean()
data10y["Rolling_200"] = data10y["Day_Avg"].rolling(window = 200, min_periods=1).mean()
# print(data10y)

compare = st.multiselect("I want to compare below factors",
                         data10y.columns,
                         default= ("Day_Avg", "Rolling_20","Rolling_200") )
# compare = ["Day_Avg", "Rolling_20","Rolling_200"]

# Start plotting
fig = px.line(data_frame= data10y, y= compare, 
              title= f"{ticker} security Price {period}")
# fig.write_html("./Finboard/Day_Avg.html", include_plotlyjs="cdn")
st.plotly_chart(fig)

data10y_vol = data10y.copy()
data10y_vol["rolling_vol"] = data10y_vol["Volume"].rolling(window = 200, min_periods=1).mean()
fig_vol = px.line(data10y_vol, y=data10y_vol["rolling_vol"]  ,  
              title= f"{ticker}'s {period} Volume (rolling_200)")


st.write( f"{ ticker_list['Name'][ticker_list['Ticker']==ticker].item()  }'s {period} share overview")
st.data_editor(data10y_vol)

# ticker_list.at

############ END