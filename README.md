# Time-Series Stock & ETF Forecast Streamlit Application


### Technical Description in Non-Technical Terms
This application forecasts individual stock and exchange-traded fund (ETF) prices. Select a ticker (abbreviation for specific company stock or investment vehicle) - Apple (AAPL) is selected by default. A trained Keras LSTM (Long Short Term Memory) model performs the calculations associated with the prediction (estimations based on historical data from Yahoo Finance) of future prices. This web app contains 503 stocks that serve as S&P 500 components plus the top 25 USD-Volume leaders (such as IVV - an S&P 500 ETF) - hence a total of 528 options available. DISCLAIMER - The developer of this tool is not a Financial Advisor, therefore live trading-related decisions solely based on the outputs from this application are not encouraged.

### Presentation GIF
<img src="Assets/stock_prediction.gif" width="80%">

1. Python 3.8 Requirements for Web / Machine Learning App:
   * keras==2.11.0
   * matplotlib==3.6.3
   * numpy==1.21.6
   * pandas==1.5.3
   * pandas_datareader==0.10.0
   * plotly==5.14.1
   * scikit_learn==1.2.2
   * seaborn==0.12.2
   * streamlit==1.20.0
   * yfinance==0.2.17
   
2. Knowledge required for the completion of this project: 
   * Basic Calculus (Time Series) & Statistics
   * Financial Markets & Investment Vehicles - Stocks, ETFs, S&P 500 - Index Funds 
   * Python Programming using Visual Studio Code
   * Shell Scripting Programming (for dependencies' installation and Python downgrading)
   * Keras LSTM (Long Short Term Memory) layer (Recurrent Neural Network) for timeseries prediction
   * Web Development & Application Deployment
