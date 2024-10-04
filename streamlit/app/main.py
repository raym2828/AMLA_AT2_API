import streamlit as st
import requests

st.title('Hello World!')

try:
    request = requests.get(f'http://localhost:8000/health')
    if request.status_code != 200:
        st.write('API is down!')
        st.stop()
    else:
        st.write('API is up!')
except:
    st.write('API is down!')
    st.stop()
