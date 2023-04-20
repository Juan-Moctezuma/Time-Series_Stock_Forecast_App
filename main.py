######### PART 1 - IMPORT LIBRARIES
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter
import numpy as np
import pandas as pd
import pandas_datareader as data
from plotly import graph_objs as go
import seaborn as sns
from stock_etf_list import stocks
import streamlit as st
import warnings
import yfinance as yf

from keras.models import load_model
from datetime import date 
from sklearn.preprocessing import MinMaxScaler

######### PART 2 - SETTINGS
sns.set_style('darkgrid')
matplotlib.rcParams['font.size'] = 14
matplotlib.rcParams['figure.figsize'] = (9, 5)
matplotlib.rcParams['figure.facecolor'] = '#00000000'
warnings.simplefilter(action='ignore', category=FutureWarning)

######### PART 3 - APPLICATION FRONT-END UPPER SECTION
# Title
st.title('Stock & ETF Forecast Application')

# Subtitle
col1, col2 = st.columns([2,1])
with col1:
    st.markdown("## Web Application For Investors")
with col2:
    st.image('Assets/trend.png', width = 50)
st.markdown("***")
st.markdown("This application forecasts individual stock and exchange-traded fund (ETF) prices. " + 
            "Select a ticker (abbreviation for specific company stock or investment vehicle) and use the slider " + 
            "to choose a prediction timeframe (ranging from 1 to 4 years). Facebook's Prophet library is the software " + 
            "that performs the calculations associated with the prediction (estimations based on historical data from Yahoo Finance) " + 
            "of future prices. This web app contains 503 stocks that serve as S&P 500 components plus the top 25 USD-Volume " + 
            "leaders (such as IVV - an S&P 500 ETF) - hence a total of 528 options available. " +
            "There's a predicted price (1 day into the future) for the share associated with your selected ticker at the bottom of the page. ")
st.markdown("**DISCLAIMER - The developer of this tool is not a Financial Advisor, therefore live trading-related decisions solely based on the outputs from this application are not encouraged.**")
            
st.markdown("***")

TODAY = date.today().strftime("%Y-%m-%d")

# Define function for loading data
def load_data(ticker):
    START = "2010-01-01"
    TODAY = date.today().strftime("%Y-%m-%d")
    data = yf.download(ticker, START, TODAY)
    data.reset_index(inplace = True)
    return data

stock_ticker = st.selectbox('Select Ticker Dataset', stocks)
st.markdown("***")

######### PART 3 - APPLICATION FRONT-END MIDDLE SECTION
#### TABLE 1 (ALL DATA)
st.subheader(stock_ticker + ' - Data From 2010-01-04 To ' + TODAY)
data = load_data(stock_ticker)
st.write(data)

#### TABLE 2 (STATS)
st.subheader(stock_ticker + ' - Statistical Data')
st.write(data.describe())

#### GRAPH 3 
def plot_raw_data():
	fig = go.Figure()
	fig.add_trace(go.Scatter(x = data['Date'], y = data['Open'], name = "stock_open"))
	fig.add_trace(go.Scatter(x = data['Date'], y = data['Close'], name = "stock_close"))
	fig.layout.update(xaxis_rangeslider_visible = True, plot_bgcolor = "white")
	st.plotly_chart(fig)
	
st.subheader(stock_ticker + ' - Time Series Data With Range-Slider')
plot_raw_data()

#### GRAPH 4
st.subheader('Closing Price VS. Time Chart: With 100 SMA & 200 SMA')
st.write("A 100-day and 200-day Moving Average (MA) is the average of closing prices of the previous 100 days and 200 days respectively. " + 
         "According to market experts - the 'buying signal' appears when SMA-100 line cuts into SMA-200's line in its way upward. ")
ma100 = data.Close.rolling(100).mean()
ma200 = data.Close.rolling(200).mean()
fig = plt.figure(figsize = (12,6))
plt.plot(data.Close, 'b', label = 'Closing Price')
plt.plot(ma100, 'r', label = '100 SMA')
plt.plot(ma200, 'g', label = '200 SMA')
plt.xlabel('Time')
plt.ylabel('Close Price USD ($)')
plt.legend()
st.pyplot(fig)

#### GRAPH 5 - PREDICTION
#Loading Model
m = load_model('keras_model.h5')

# Splitting Data Into Training And Testing
data_training = pd.DataFrame(data['Close'][0:int(len(data)*0.70)])
data_testing = pd.DataFrame(data['Close'][int(len(data)*0.70): int(len(data))])

scaler = MinMaxScaler(feature_range = (0,1))
data_training_array = scaler.fit_transform(data_training)

#Testing Model
past_100_days = data_training.tail(100)
final_df = past_100_days.append(data_testing, ignore_index = True)
input_data = scaler.fit_transform(final_df)

x_test = []
y_test = []

for i in range(100, input_data.shape[0]):
  x_test.append(input_data[i - 100: i])
  y_test.append(input_data[i,0])

x_test, y_test = np.array(x_test), np.array(y_test)
y_pred = m.predict(x_test)
y_predicted = y_pred /scaler.scale_
y_test = y_test /scaler.scale_

st.subheader('Original Price VS. Predicted Price')
fig2 = plt.figure(figsize = (12,6))
plt.plot(y_test, 'b', label = 'Original Price')
plt.plot(y_predicted, 'r', label = 'Predicted Price')
plt.xlabel('Time')
plt.ylabel('Close Price USD ($)')
plt.legend()
st.pyplot(fig2)

######### PART 4 - APPLICATION FRONT-END BOTTOM SECTION
# Predict for tomorrow (using last 200 days)
last_200_days = (data['Close'][-200:]).values
last_200_days_scaled = scaler.transform(last_200_days.reshape(-1,1))

next_day_test = []
next_day_test.append(last_200_days_scaled)
next_day_test = np.array(next_day_test)
next_day_test = np.reshape(next_day_test, (next_day_test.shape[0], next_day_test.shape[1], 1))
pred_price = m.predict(next_day_test)
pred_price = scaler.inverse_transform(pred_price)
pred_price = round(float(pred_price), 2)
st.subheader('Predicted price for 1 day into the future (upcoming business day) for 1 ' + stock_ticker + ' share is approximately: ' + str(pred_price) + ' $')

# Ending Section
st.markdown("")
st.markdown("")
st.caption("Machine Learning Product Made by Juan L. Moctezuma-Flores")

################################### END OF APPLICATION ###################################