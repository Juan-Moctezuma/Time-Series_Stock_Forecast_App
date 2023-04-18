# Time-Series Stock & ETF Forecast Streamlit Application


### Technical Description in Non-Technical Terms
This Streamlit (platform's name) application forecasts individual stock and exchange-traded fund (ETF) prices. Select a ticker (abbreviation for specific company stock or investment vehicle) and use the slider to choose a prediction timeframe (ranging from 1 to 4 years). Facebook's Prophet library is the software that performs the calculations associated with the prediction (estimations based on historical data from Yahoo Finance) of future prices. This web app contains 503 stocks that serve as S&P 500 components plus the top 25 USD-Volume leaders (such as IVV - an S&P 500 ETF) - hence a total of 528 options available. You may download the forecast graph (in HTML format) at the bottom of the page. DISCLAIMER - The developer of this tool is not a Financial Advisor, therefore live trading-related decisions solely based on the outputs from this application are not encouraged.

### Presentation GIF

### WARNING: DUE TO MEMORY-RELATED ISSUES FROM STREAMLIT CLOUD PLATFORM - THE APP DOESN'T WORK ON MOBILE DEVICES
<b>Click the following link to open the App:</b>

1. Python 3.8 Requirements for Web / Machine Learning App:
   * fbprophet==0.7.1
   * pandas==1.5.3
   * plotly==5.14.1
   * streamlit==1.20.0
   * yfinance==0.2.17
   
2. Knowledge required for the completion of this project: 
   * Basic Calculus (Time Series) & Statistics
   * Financial Markets & Investment Vehicles - Stocks, ETFs, S&P 500 - Index Funds 
   * Python Programming using Visual Studio Code
   * Shell Scripting Programming (for dependencies' installation and Python downgrading)
   * Web Development & Application Deployment
