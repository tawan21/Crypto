import streamlit as st
import pandas as pd

def app():
    st.header('**Your Crypto Holdings**')

    df = pd.read_json('https://api.binance.com/api/v3/ticker/24hr')
    options = st.multiselect(
        'Select upto 6 Currencies',
        df,
        ['BTCBUSD', 'ETHBUSD']
    )
    col1, col2, col3 = st.columns(3)
    with col1:
        opt = st.selectbox('', options)
    with col2:
        st.text('')
        st.text('')
        inc = st.button('BUY')
    with col3:
        st.text('')
        st.text('')
        dec = st.button('SELL')
    n = len(options)
    st.text('')
    if opt[:4] not in st.session_state:
        st.session_state[opt[:4]] = 0
    if inc:
        st.session_state[opt[:4]] += 1
        st.session_state[opt] -= float(df[df.symbol == opt].weightedAvgPrice)
    if dec:
        st.session_state[opt[:4]] -= 1
        st.session_state[opt] += float(df[df.symbol == opt].weightedAvgPrice)
    col1, col2 = st.columns(2)
    if n >= 1:
        if options[0] not in st.session_state:
            st.session_state[options[0]] = 0
        with col1:
            col1.metric(options[0], df[df.symbol == options[0]].weightedAvgPrice, st.session_state[options[0]])
    if n >= 2:
        if options[1] not in st.session_state:
            st.session_state[options[1]] = 0
        with col2:
            col2.metric(options[1], df[df.symbol == options[1]].weightedAvgPrice, st.session_state[options[1]])
    if n >= 3:
        if options[2] not in st.session_state:
            st.session_state[options[2]] = 0
        with col1:
            col1.metric(options[2], df[df.symbol == options[2]].weightedAvgPrice, st.session_state[options[2]])
    if n >= 4:
        if options[3] not in st.session_state:
            st.session_state[options[3]] = 0
        with col2:
            col2.metric(options[3], df[df.symbol == options[3]].weightedAvgPrice, st.session_state[options[3]])
    if n >= 5:
        if options[4] not in st.session_state:
            st.session_state[options[4]] = 0
        with col1:
            col1.metric(options[4], df[df.symbol == options[4]].weightedAvgPrice, st.session_state[options[4]])
    if n >= 6:
        if options[5] not in st.session_state:
            st.session_state[options[5]] = 0
        with col2:
            col2.metric(options[5], df[df.symbol == options[5]].weightedAvgPrice, st.session_state[options[5]])
    if n > 6:
        st.warning('You have added the maximum of Six Coins!')
    with col2:
        st.metric('Pending SELL Calls', st.session_state[opt[:4]])