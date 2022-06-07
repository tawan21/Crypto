import pandas as pd
import streamlit as st

def app():
    st.header('**Selected Tickers**')

    df = pd.read_json('https://api.binance.com/api/v3/ticker/24hr')

    def roundVal(val):
        if val.values > 1:
            rounded = float(round(val, 2))
        else:
            rounded = float(round(val, 8))
        return rounded

    col1, col2, col3 = st.columns(3)

    sel1 = st.sidebar.selectbox('Ticker 1', df.symbol, list(df.symbol).index('BTCBUSD'))
    sel2 = st.sidebar.selectbox('Ticker 2', df.symbol, list(df.symbol).index('ETHBUSD'))
    sel3 = st.sidebar.selectbox('Ticker 3', df.symbol, list(df.symbol).index('BNBBUSD'))
    sel4 = st.sidebar.selectbox('Ticker 4', df.symbol, list(df.symbol).index('XRPBUSD'))
    sel5 = st.sidebar.selectbox('Ticker 5', df.symbol, list(df.symbol).index('ADABUSD'))
    sel6 = st.sidebar.selectbox('Ticker 6', df.symbol, list(df.symbol).index('DOGEBUSD'))
    sel7 = st.sidebar.selectbox('Ticker 7', df.symbol, list(df.symbol).index('SHIBBUSD'))
    sel8 = st.sidebar.selectbox('Ticker 8', df.symbol, list(df.symbol).index('DOTBUSD'))
    sel9 = st.sidebar.selectbox('Ticker 9', df.symbol, list(df.symbol).index('MATICBUSD'))

    tick1_df = df[df.symbol == sel1]
    tick2_df = df[df.symbol == sel2]
    tick3_df = df[df.symbol == sel3]
    tick4_df = df[df.symbol == sel4]
    tick5_df = df[df.symbol == sel5]
    tick6_df = df[df.symbol == sel6]
    tick7_df = df[df.symbol == sel7]
    tick8_df = df[df.symbol == sel8]
    tick9_df = df[df.symbol == sel9]

    tick1_price = roundVal(tick1_df.weightedAvgPrice)
    tick2_price = roundVal(tick2_df.weightedAvgPrice)
    tick3_price = roundVal(tick3_df.weightedAvgPrice)
    tick4_price = roundVal(tick4_df.weightedAvgPrice)
    tick5_price = roundVal(tick5_df.weightedAvgPrice)
    tick6_price = roundVal(tick6_df.weightedAvgPrice)
    tick7_price = roundVal(tick7_df.weightedAvgPrice)
    tick8_price = roundVal(tick8_df.weightedAvgPrice)
    tick9_price = roundVal(tick9_df.weightedAvgPrice)

    tick1_percent = f'{float(tick1_df.priceChangePercent)}%'
    tick2_percent = f'{float(tick2_df.priceChangePercent)}%'
    tick3_percent = f'{float(tick3_df.priceChangePercent)}%'
    tick4_percent = f'{float(tick4_df.priceChangePercent)}%'
    tick5_percent = f'{float(tick5_df.priceChangePercent)}%'
    tick6_percent = f'{float(tick6_df.priceChangePercent)}%'
    tick7_percent = f'{float(tick7_df.priceChangePercent)}%'
    tick8_percent = f'{float(tick8_df.priceChangePercent)}%'
    tick9_percent = f'{float(tick9_df.priceChangePercent)}%'

    col1.metric(sel1, tick1_price, tick1_percent)
    col2.metric(sel2, tick2_price, tick2_percent)
    col3.metric(sel3, tick3_price, tick3_percent)
    col1.metric(sel4, tick4_price, tick4_percent)
    col2.metric(sel5, tick5_price, tick5_percent)
    col3.metric(sel6, tick6_price, tick6_percent)
    col1.metric(sel7, tick7_price, tick7_percent)
    col2.metric(sel8, tick8_price, tick8_percent)
    col3.metric(sel9, tick9_price, tick9_percent)

    st.header('**All Coins**')
    st.dataframe(df)