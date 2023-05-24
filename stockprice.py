import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import yfinance as yf
st.title('stock prices application')

def get_stock_data(ticker, start_date, end_date):
    data = yf.download(ticker, start=start_date, end=end_date)
    return data

ticker = st.sidebar.text_input("Enter Stock Ticker Symbol")
start_date = st.sidebar.date_input("Start Date")
end_date = st.sidebar.date_input("End Date")
data = get_stock_data(ticker, start_date, end_date)
data = data.rename(columns={'Adj Close': 'Adj_Close'})
fig=px.line(data,x=data.index,y=data['Adj_Close'],title=ticker)
st.plotly_chart(fig)
menu=st.sidebar.selectbox('Menu',['price movement','stationarity'])
if menu== 'price movement':
    st.header('price movement')
    data2=data.copy()
    data2['% Adj Close change']=data2['Adj_Close']/data2['Adj_Close'].shift(1)-1
    data2.dropna(inplace=True)
    st.write(data2)
    annual_return=data2['% Adj Close change'].mean()*252*100
    st.write('Annual Return is',annual_return,'%')
    stdev=np.std(data2['% Adj Close change'])*np.sqrt(252)
    st.write('Standard Deviation is',stdev*100,'%')
    st.write('Risk Adj close.Return is',annual_return/(stdev*100))

if menu== 'stationarity': 

    
    import plotly.graph_objs as go
    from statsmodels.tsa.stattools import adfuller
    data2=data.copy()

    def raw_plot_data():
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=data2.index, y=data2['Open'], name=f'{ticker} Stock Open',line_color='red'))
        fig.add_trace(go.Scatter(x=data2.index, y=data2['Close'], name=f'{ticker} Stock Close'))
        fig.layout.update(title_text='Time Series Data',xaxis_rangeslider_visible=True) 
        st.plotly_chart(fig)
    raw_plot_data()

    rolling_mean = data2['Adj_Close'].rolling(window=12).mean()
    rolling_std = data2['Adj_Close'].rolling(window=12).std()
    result = adfuller(data2['Adj_Close'])
    p_value = result[1]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data2.index, y=data2['Adj_Close'], name=f'{ticker} Stock Price'))
    fig.add_trace(go.Scatter(x=rolling_mean.index, y=rolling_mean, name='Rolling Mean'))
    fig.add_trace(go.Scatter(x=rolling_std.index, y=rolling_std, name='Rolling Std'))

    if p_value < 0.05:
        fig.add_annotation(xref="paper", yref="paper",
                        x=0.95, y=1.1,
                        text=f"ADF test p-value: {p_value:.4f} (Stationary)",
                        showarrow=False,
                        bgcolor="green", font=dict(color="white"))
    else:
        fig.add_annotation(xref="paper", yref="paper",
                        x=0.95, y=1.1,
                        text=f"ADF test p-value: {p_value:.4f} (Non-stationary)",
                        showarrow=False,
                        bgcolor="red", font=dict(color="white"))

    fig.update_layout(title=f'{ticker} Stock Stationarity Analysis',
                  xaxis_title='Date',
                  yaxis_title='Adj Closing Price',
                  legend=dict(yanchor="top", y=1.19, xanchor="left", x=0.01))

    st.plotly_chart(fig) 

    






    


    

    
    
