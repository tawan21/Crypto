import pandas as pd
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas_datareader as web
import datetime as dt
from sklearn.preprocessing import MinMaxScaler
from tensorflow.python.keras.layers import Dense, Dropout, LSTM
from tensorflow.python.keras.models import Sequential

def MA(data, period):
    return pd.Series(data).rolling(period).mean()

CHOICES = {
    'Shiba Inu': 'SHIB',
    'Bitcoin': 'BTC',
    'Ethereum': 'ETH',
    'Dogecoin': 'DOGE'
}

@st.cache()
def lstm(crypto):
    against = 'USD'
    start = dt.datetime(2016, 1, 1)
    end = dt.datetime.now()
    data = web.DataReader(f'{crypto}-{against}', 'yahoo', start, end)

    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(data['Close'].values.reshape(-1, 1))

    days = 60
    future_days = 30

    x_train, y_train = [], []
    for x in range(days, len(scaled_data) - future_days):
        x_train.append(scaled_data[x - days:x, 0])
        y_train.append(scaled_data[x + future_days, 0])
    x_train, y_train = np.array(x_train), np.array(y_train)
    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

    model = Sequential()
    model.add(LSTM(units=50, return_sequences=True, input_shape = (x_train.shape[1], 1)))
    model.add(Dropout(0.2))
    model.add(LSTM(units=50, return_sequences=True))
    model.add(Dropout(0.2))
    model.add(LSTM(units=50))
    model.add(Dropout(0.2))
    model.add(Dense(units=1))
    model.compile(optimizer='adam', loss='mean_squared_error')
    model.fit(x_train, y_train, epochs=25, batch_size=32)

    test_start = dt.datetime(2020, 1, 1)
    test_end = dt.datetime.now()
    test_data = web.DataReader(f'{crypto}-{against}', 'yahoo', test_start, test_end)
    actual_prices = test_data['Close'].values
    total_dataset = pd.concat((data['Close'], test_data['Close']), axis=0)
    model_inputs = total_dataset[len(total_dataset) - len(test_data) - days:].values
    model_inputs = model_inputs.reshape(-1, 1)
    model_inputs = scaler.fit_transform(model_inputs)

    x_test = []
    for x in range(days, len(model_inputs)):
        x_test.append(model_inputs[x - days:x, 0])
    x_test = np.array(x_test)
    x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

    prediction_prices = model.predict(x_test)
    prediction_prices = scaler.inverse_transform(prediction_prices)
    
    return actual_prices, prediction_prices

def app():
    st.sidebar.title('Pick One Crypto')
    selection = st.sidebar.radio('', list(CHOICES.keys()))
    crypto = CHOICES[selection]
    
    st.header('**LSTM Prediction**')
    actual_prices, prediction_prices = lstm(crypto)

    fig = plt.figure(figsize = (20, 10))
    plt.plot(actual_prices, label = 'Actual Price')
    plt.plot(prediction_prices, label = 'Predicted Price after 30 days')
    plt.legend(fontsize = 16)
    st.pyplot(fig)

    test_start = dt.datetime(2020, 1, 1)
    test_end = dt.datetime.now()
    test_data = web.DataReader(f'{crypto}-USD', 'yahoo', test_start, test_end)

    test_data['MA20'] = MA(test_data['Close'], 20)
    test_data['MA50'] = MA(test_data['Close'], 50)
    test_data.dropna(inplace = True)
    test_data['SHORT_GR_LONG'] = np.where(test_data['MA20'] > test_data['MA50'], 1, 0)
    test_data['Signal'] = test_data['SHORT_GR_LONG'].diff()

    st.header('**Moving Average Prediction**')
    fig = plt.figure(figsize = (20, 10))
    test_data['Close'].plot(label = 'Close Price', color = 'k')
    test_data['MA20'].plot(label = '20-day Moving Average', color = 'b')
    test_data['MA50'].plot(label = '50-day Moving Average', color = 'g')
    plt.plot(test_data[test_data['Signal'] == 1].index, test_data['MA20'][test_data['Signal'] == 1], '^', markersize = 15, color = 'g', label = 'Buy')
    plt.plot(test_data[test_data['Signal'] == -1].index, test_data['MA20'][test_data['Signal'] == -1], 'v', markersize = 15, color = 'r', label = 'Sell')
    plt.legend(fontsize = 16)
    st.pyplot(fig)