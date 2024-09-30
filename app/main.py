from fastapi import FastAPI, Query, HTTPException
from starlette.responses import JSONResponse
from pydantic import BaseModel, Field
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

# # Define a constrained date type with the desired range
# ConstrainedDate = condate(ge=date(2015, 4, 18), le=date(2020, 12, 31))

# # Create a Pydantic model to validate the input data
# class User_input(BaseModel):
#     # target_date: date = Field(..., format="YYYY-MM-DD", ge="2015-04-18", le="2020-12-31") 
#     target_date: ConstrainedDate = Field(..., description="Date must be between 2015-04-18 and 2020-12-31")


# class forecast_output(BaseModel):
#     ds: date
#     yhat: float     
    

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

# @app.post("/validate_date/")
# def validate_date(user_input: User_input):
#     try:
#         return {"message": "Date is valid", "target_date": user_input.target_date}
#     except ValidationError as e:
#         raise HTTPException(status_code=422, detail=str(e))
    

# @app.get("/predict/")
# def predict(target_date: date ):
    
#     return {"message": "Date is valid", "target_date": target_date}
@app.get("/sales/national")
def predict(target_date: date = Query(..., description="Target date for sales forecasting must be beween 2015-04-18 and 2020-12-31")):
    if not (date(2015, 4, 18) <= target_date <= date(2020, 12, 31)):
        raise HTTPException(status_code=422, detail="Date must be between 2015-04-18 and 2020-12-31")
    
    target_date= pd.to_datetime(target_date)
    target_date_end = target_date + pd.Timedelta(days=7)
    last_date=pd.to_datetime('2015-04-18') 
    days_to_forecast=(target_date_end - last_date).days
    days_to_forecast
    future = m.make_future_dataframe(periods=days_to_forecast, freq='D')   # Create a future DataFrame
    forecast = m.predict(future)   
    forecast_api=forecast[['ds','yhat']].tail(7)
    forecast_api['ds'] = forecast_api['ds'].dt.date
    forecast_dict = forecast_api.set_index('ds')['yhat'].to_dict()
    return forecast_dict

