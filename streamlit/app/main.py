import streamlit as st
import requests

st.title('Hello World!')

try:
    request = requests.get(f'https://fast-api-1-0.onrender.com/health')
    if request.status_code != 200:
        st.write('API is down!')
        st.stop()
    else:
        st.write('API is up!')
except:
    st.write('API is down!')
    st.stop()
