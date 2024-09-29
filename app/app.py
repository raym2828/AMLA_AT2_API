import streamlit as st
import json
import requests

st.title('ML Streamlit App')
st.write("""
## The Machine Learning App

You can use this application in order to get predictions from a trained Adaboost model on the estimated number of shares for a news article.

You will have to select the values that describe a news article.
""")

# taking user input
option = st.selectbox('What operation would you like to perform?',
                      ('add','subtract','multiply','divide'))
st.write("Select the numbers from slider below")
x = st.slider("X",0,100,20)
y= st.slider("Y",0,130, 10)

#converting to json format
inputs={"operation":option,"x":x,"y":y}

#when the user clicks on button it will fetch API
if st.button("Calculate"):
    response = requests.post("http://127.0.0.1:8000/calculate",data= json.dumps(inputs))

    st.subheader(f"Response from API = {response.text}")