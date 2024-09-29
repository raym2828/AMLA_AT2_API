from fastapi import FastAPI
from starlette.responses import JSONResponse
from pydantic import BaseModel
from datetime import date

# from joblib import load
import pandas as pd
import numpy as np
import sys
import subprocess

# Print Python version and executable path
print(f"Python version: {sys.version}")
print(f"Python executable: {sys.executable}")

# List installed packages
installed_packages = subprocess.check_output([sys.executable, '-m', 'pip', 'list']).decode('utf-8')
print(f"Installed packages:\n{installed_packages}")

# Alias np.float_ to np.float64 to handle compatibility with NumPy 2.0
np.float_ = np.float64

try:
    from prophet import Prophet
    from prophet.serialize import model_to_json, model_from_json
    print("Successfully imported Prophet")
except ImportError as e:
    print(f"Error importing Prophet: {e}")


# Create a Pydantic model to validate the input data
class User_input(BaseModel):
    target_date: date 

class forecast_output(BaseModel):
    forecast: dict     
    

# Load the forecast model
with open('./models/prophet_serialized_model.json', 'r') as fin:
    m = model_from_json(fin.read())  # Load model

# Create a FastAPI instance
app = FastAPI()

################################################################
# Define the API endpoints                                     #
################################################################
@app.get("/")
def read_root():
    return {'message': 'This is the sales prediction and forecasting tool for American Retailer Co.'}

@app.get("/health", status_code=200)
def healthcheck():
    return'Ready to Predict and Forecast Sales'

@app.get("/sales/national")
def predict(target_date='2015-05-19'):
    target_date= pd.to_datetime(target_date)
    target_date_end = target_date + pd.Timedelta(days=7)
    last_date=pd.to_datetime('2015-04-25') #####Plz UPDATE
    days_to_forecast=(target_date_end - last_date).days
    days_to_forecast
    future = m.make_future_dataframe(periods=days_to_forecast, freq='D')   # Create a future DataFrame for 12 months
    forecast = m.predict(future)   
    forecast_api=forecast[['ds','yhat']].tail(7)
    return forecast_api.to_dict(orient='records')

