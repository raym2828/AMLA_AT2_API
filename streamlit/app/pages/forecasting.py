import streamlit as st
import requests

date = st.date_input('Select a date')
if date:
    if isinstance(date, tuple):
        date_str = date[0].strftime('%Y-%m-%d')
    else:
        date_str = date.strftime('%Y-%m-%d')
        response = requests.get(f"https://fast-api-1-0.onrender.com/sales/national?target_date={date_str}")
        response.raise_for_status()  # Raise an error for bad status codes
        if "error" in response:
            st.error(response["error"])
        else:
            forecast = response.json()
            st.write(forecast)
        
    
    
    # forecast = response.json()
    # st.write(forecast)