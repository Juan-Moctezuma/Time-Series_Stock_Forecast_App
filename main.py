######### PART 1 - Importing Libraries
from datetime import date
from fbprophet import Prophet
from fbprophet.plot import plot_plotly
import pandas as pd
from plotly import graph_objs as go
from stock_etf_list import stocks
import streamlit as st
import yfinance as yf

######### PART 2 - APPLICATION FRONT-END UPPER SECTION
# Title
st.title('Stock & ETF Forecast Application')

# Subtitle
col1, col2 = st.columns([2,1])
with col1:
    st.markdown("## Web Application For Investors")
with col2:
    st.image('Assets/trend.png', width = 50)

st.markdown("")
st.markdown("This application forecasts individual stock and exchange-traded fund (ETF) prices. " + 
            "Select a ticker (abbreviation for specific company stock or investment vehicle) and use the slider " + 
            "to choose a prediction timeframe (ranging from 1 to 4 years). Facebook's Prophet library is the software " + 
            "that performs the calculations associated with the prediction (estimations based on historical data from Yahoo Finance) " + 
            "of future prices. This web app contains 503 stocks that serve as S&P 500 components plus the top 25 USD-Volume " + 
            "leaders (such as IVV - an S&P 500 ETF) - hence a total of 528 options available. " +
            "You may download the forecast graph (in HTML format) at the bottom of the page. " +
            "DISCLAIMER - The developer of this tool is not a Financial Advisor, therefore live trading-related " +
            "decisions solely based on the outputs from this application are not encouraged. "
            )
st.markdown("***")

# Selectbox
selected_stock = st.selectbox('Select Ticker Dataset', stocks)

# Slider
n_years = st.slider('Years of Prediction:', 1, 4)
period = n_years * 365

######### PART 3 - APPLICATION FRONT-END MIDDLE SECTION
@st.cache_resource
# Define function for loading data
def load_data(ticker):
    START = "2010-01-01"
    TODAY = date.today().strftime("%Y-%m-%d")
    data = yf.download(ticker, START, TODAY)
    data.reset_index(inplace = True)
    return data

# Input selected stock/ETF into defined function
data = load_data(selected_stock)

# Raw Data Chart
st.subheader('Raw Data - Previous Week')
st.write(data.tail())

# Define function for plotting raw data
def plot_raw_data():
	fig = go.Figure()
	fig.add_trace(go.Scatter(x = data['Date'], y = data['Open'], name = "stock_open"))
	fig.add_trace(go.Scatter(x = data['Date'], y = data['Close'], name = "stock_close"))
	fig.layout.update(xaxis_rangeslider_visible = True, plot_bgcolor = "white")
	st.plotly_chart(fig)
	
st.subheader('Time Series Data With Range-Slider')
plot_raw_data()

# Predict forecast with Prophet.
df_train = data[['Date','Close']]
df_train = df_train.rename(columns = {"Date": "ds", "Close": "y"})

# Use timeseries' Prophet function developed by Facebook
m = Prophet()
m.fit(df_train)
future = m.make_future_dataframe(periods = period)
forecast = m.predict(future)

# Show and plot forecast
st.subheader('Forecast Data - Table')
st.write(forecast.tail())
    
if n_years == 1:
    st.subheader(f'Forecast (Prediction) Plot For {n_years} Year')
    fig1 = plot_plotly(m, forecast)
    fig1.update_layout(plot_bgcolor = "white")
    st.plotly_chart(fig1)
elif n_years > 1:
    st.subheader(f'Forecast (Prediction) Plot For {n_years} Years')
    fig1 = plot_plotly(m, forecast)
    fig1.update_layout(plot_bgcolor = "white")
    st.plotly_chart(fig1)
    
# Show and plot forecast components
st.subheader('Forecast Components - Graphs')
fig2 = m.plot_components(forecast)
st.write(fig2)
st.markdown("")
st.markdown("")

######### PART 4 - DOWNLOAD BUTTON
st.markdown("#### Download Forecast Graph in HTML Format")
export = fig1.to_html()
st.download_button(label="Download", data = export, file_name = f'{selected_stock}-{n_years}-Yr-Prediction-{date.today().strftime("%Y-%m-%d")}.html')

######### PART 5 - APPLICATION FRONT-END BOTTOM SECTION
st.markdown("")
st.markdown("")
st.caption("Machine Learning Product Made by Juan L. Moctezuma-Flores")

################################### END OF APPLICATION ###################################