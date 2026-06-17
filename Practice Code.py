import plotly.express as px
import pandas as pd
# print(pd.__version__)
import pip
print(pip.__version__)
import numpy as np
# print(np.__version__)
# in terminal, python -m pip install yfinance
import yfinance as yf
print(yf.__version__)
import sys
# Returns the root directory of the current Python environment
print(sys.prefix)
# Returns True if running in a virtual environment
print(sys.prefix != sys.base_prefix)



data_races = {
    'Race': ['Badwater', 'Barkley Marathons', 'Vero Beach Ultra', 'Forgotten Florida', 'Badwater'],
    'Year': [2020, 2021, 2020, 2021, 2025],
    'Difficulty': [9.7, 9.8, 8.1, 6.1, 9.9]
}
df_r = pd.DataFrame(data_races)
print(df_r)

# df_r.set_index(['Race', 'Year'], inplace=True)
# print(df_r)
# df_r.index
# df_r.index.get_level_values(0)

# del dat

dat = yf.Ticker("MSFT")

# get historical market data
dat.history(period='1mo')

# options
dat.option_chain(dat.options[0]).calls

# get financials
dat.balance_sheet
dat.quarterly_income_stmt

# dates
dat.calendar

# general info
dat.info

# analysis
dat.analyst_price_targets

# websocket
# dat.live() # continuous listening starts

# print( dat) # not print- friendly

dat_1mo = dat.history(period='1mo')
print(dat_1mo)

dat_1mo.index # type datetyme64
dat_1mo[dat_1mo["High"]>485] # good approach for getting T/F for every row
dat_1mo.loc["2025-12-29 00:00:00-05:00"]
dat_1mo.loc["29-12-2025"]
dat_1mo.loc["29-12-2025"]
dat_1mo.loc["12/29/2025"]
dat_1mo.loc["29/12/2025"]
dat_1mo.loc["29.12.2025"]
dat_1mo.loc["29.12.2025"]
# dat_1mo["2025-12-29 00:00:00-05:00"] # can't, this approach is for columns

df = pd.DataFrame({'User_id': ['234', '738', '632', '777', '834', '123'],
                   'Age': [11, 45, 56, 32, 26, 31],
                   'Hourly': [100, 93, 78, 120, 64, 115],
                   'FT_Team': ['Steelers', 'Seahawks', 'Falcons', 'Falcons', 'Patriots', 'Steelers']})

df[ (df["Age"]<40) & (df["Hourly"] >=100)   ]
df.loc[ (df["Age"]<40) & (df["Hourly"] >=100)   ]

df["FT_Team"].str.contains("^S")
df.loc[ (df["Age"]<40) & (df["Hourly"] >=100) & df["FT_Team"].str.contains("^S")]

df[ [ "User_id", "FT_Team" ] ] # list of col names to get selected cols


# date filtering
dat_1mo_v2 = dat_1mo.reset_index(inplace=False)
dat_1mo_v2[ ( dat_1mo_v2["Date"] > "2025-12-10") & (dat_1mo_v2["Date"] < "2025-12-05" ) ]

# Rolling Average
dat_1mo_v2["Avg"] = (dat_1mo_v2["High"] + dat_1mo_v2["Low"])/2

# If we want to eval rolling average over time:
dat_1mo_v2["Rolling_Avg"] = dat_1mo_v2["Avg"].rolling(window=5).mean()

# If we want to eval rolling average over all df:
dat_1mo_v2["Rolling_Avg"] = dat_1mo_v2["Avg"].expanding().mean()
# type(dat_1mo_v2["Avg"].rolling(window=5).mean()) # series
print( dat_1mo_v2 )
# in terminal, python -m pip install plotly

# reorder the cols
dat_1mo_v2.iloc[: , [ 1,2,3,4,5,6,7 , 9, 8] ]
print( dat_1mo_v2.head())

### dataset

data = yf.Ticker("NVDA")

# get historical market data
data10y = data.history(period='10y')


data10y["Avg"] = (data10y["Open"] + data10y["Close"])/2
data10y["Rolling_Avg"] = data10y["Avg"].rolling(window = 20, min_periods=1).mean()
data10y["Rolling_200"] = data10y["Avg"].rolling(window = 200, min_periods=1).mean()
print(data10y)

data10y.rename(columns = {"Rolling_Avg": "Rolling_20"} , inplace=True)
data10y.rename(columns = {"Avg": "Day_Avg"} , inplace=True)


fig = px.line(data_frame= data10y, y= ["Day_Avg", "Rolling_20","Rolling_200"], 
              title= "NVDA security Price_10y")

# fig.write_html("./Finboard/Day_Avg.html", include_plotlyjs="cdn")

data10y_vol = data10y.copy()
data10y_vol["rolling_vol"] = data10y_vol["Volume"].rolling(window = 200, min_periods=1).mean()
fig_vol = px.line(data10y_vol, y=data10y_vol["rolling_vol"]  ,  
              title= "NVDA tx Volume _10y (rolling_200)")

# fig_vol.write_html("./Finboard/NVDA trade by Vol.html", include_plotlyjs="cdn")

###########
# data10y["Stock Splits"].describe()

# fig_split = px.histogram(data10y, x= "Stock Splits")
# fig_split.write_html("./Finboard/fig_split.html", include_plotlyjs="cdn")

# data10y_scatt = data10y [data10y["Stock Splits"] > 0 ]
# concluded that there was no effect to stck val or vol by the stck split
###########

# continue with streamlit python -m pip install streamlit
# import streamlit as st (in the script run for the app)