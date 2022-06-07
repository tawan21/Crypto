import streamlit as st
from multiapp import MultiApp
import dashboard
import pred
import pf

app = MultiApp()

st.markdown('''# **Crypto Dashboard**
A clean web app that helps users in predicting, visualizing and managing Cryptocurrencies.''')

app.add_app('Dashboard', dashboard.app)
app.add_app('Predictor', pred.app)
app.add_app('Portfolio', pf.app)
app.run()

st.info('*Created by Group **G-40** for Minor Project.*')