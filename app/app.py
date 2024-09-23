import streamlit as st

st.title('ML Streamlit App')
st.write("""
## The Machine Learning App

You can use this application in order to get predictions from a trained Adaboost model on the estimated number of shares for a news article.

You will have to select the values that describe a news article.
""")

timedelta                = st.slider("timedelta", 0, 750, 340)
n_tokens_title           = st.slider("n_tokens_title", 0, 25, 10)