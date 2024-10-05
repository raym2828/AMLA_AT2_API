import streamlit as st
import requests
import time

st.title('Hello World!')

while True:
    try:
        request = requests.get(f'https://fast-api-1-0.onrender.com/health')
        if request.status_code != 200:
            st.write('API is down!', 'Click [here](https://fast-api-1-0.onrender.com/) to check/fix the API.')
            time.sleep(30)
        else:
            st.write('API is up!')
            break
    except:
        st.write('API is down!')
        time.sleep(30)
