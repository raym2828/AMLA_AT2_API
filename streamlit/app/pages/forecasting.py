import streamlit as st
import requests

date = st.date_input('Select a date')
if date:
    if isinstance(date, tuple):
        date_str = date[0].strftime('%Y-%m-%d')
    else:
        date_str = date.strftime('%Y-%m-%d')
        response = requests.get(f"https://fast-api-1-0.onrender.com/sales/national?target_date={date_str}")
     
    forecast = response.json()
    st.write(forecast)