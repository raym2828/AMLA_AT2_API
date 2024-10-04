import streamlit as st
import requests

date = st.date_input('Select a date')
item_id = st.text_input('Enter the item_id')
store_id = st.text_input('Enter the store_id')

button = st.button('Predict')

if button:
    if isinstance(date, tuple):
        date_str = date[0].strftime('%Y-%m-%d')
    else:
        date_str = date.strftime('%Y-%m-%d')

    response = requests.get(f"http://0.0.0.0:8000/sales/stores/items?target_date={date_str}&item_id={item_id}&store_id={store_id}")

    prediction = response.json()
    st.write(prediction)