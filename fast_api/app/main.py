# Import the required libraries
import datetime
from fastapi import FastAPI, Query, HTTPException
from datetime import date
import pandas as pd
import numpy as np
from pydantic import BaseModel, ValidationError, validator
import xgboost as xgb
np.float_ = np.float64 
from prophet.serialize import model_to_json, model_from_json
import json

from ml_stuff.models.xgboost_model_sales import sales_predict # Import the sales_predict function

from ml_stuff.models.prophet_model_forecaster import sales_forecast # Import the sales_forecast function

# Load calendar events
df_calendar_events = pd.read_csv('ml_stuff/data/calendar_events.csv', dtype={
    'event_name': 'str',
    'event_type': 'str'
}, parse_dates=['date'])

# Load the category mappings
with open('ml_stuff/models/transformations/category_mappings.json', 'r') as f:
    category_mappings = json.load(f)

# Load the forecast model
with open('ml_stuff/models/forecasting/prophet_serialized_model.json', 'r') as fin:
    m = model_from_json(fin.read())  # Load model

# Load the predict model
model = xgb.Booster()
model.load_model('ml_stuff/models/predictive/xgb_revenue_predictor.model')

# Create a Pydantic model to validate the input data
class PredictionInput(BaseModel):
    target_date: datetime.date
    item_id: str
    store_id: str

    @validator('item_id')
    def validate_item_id(cls, v):
        if v not in category_mappings['item_id']:
            raise ValueError(f'Invalid item_id: {v}. ')
        return v

    @validator('store_id')
    def validate_store_id(cls, v):
        if v not in category_mappings['store_id']:
            raise ValueError(f'Invalid store_id: {v}.')
        return v


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

# Define the forecast endpoint
@app.get("/sales/national")
def forecast(
    target_date: date = Query(
        example="2015-12-25",
        description="Target date for sales forecasting must be beween 2015-04-18 and 2020-12-31",
    )
):
    if not (date(2015, 4, 18) <= target_date <= date(2020, 12, 31)):
        raise HTTPException(
            status_code=422, detail="Date must be between 2015-04-18 and 2020-12-31"
        )
    try:
        forecast = sales_forecast(target_date, m)
        return forecast
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

# Define the predict endpoint
@app.get("/sales/stores/items")
async def predict(
    # Inputs into predict with default values for ease of use
    target_date: date = Query(
        example="2015-12-25",
        title="Target Date",
        description="The target date for the prediction in YYYY-MM-DD format.",
    ),
    item_id: str = Query(
        example="FOODS_3_301",
        description="The item ID for the prediction.",
    ),
    store_id: str = Query(
        example="CA_1",
        description="The store ID for the prediction.",
    ),
):
    # Check for missing inputs
    for param, name in [
        (target_date, "target_date"),
        (item_id, "item_id"),
        (store_id, "store_id"),
    ]:
        if param is None:
            raise HTTPException(status_code=400, detail=f"{name} is required")
    try:
        # Validate input format matches pydantic class
        input_data = PredictionInput(
            target_date=target_date, item_id=item_id, store_id=store_id
        )
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=json.loads(e.json()))

    try:
        predict = sales_predict(
            df_calendar_events=df_calendar_events,
            category_mappings=category_mappings,
            model=model,
            target_date=target_date,
            item_id=item_id,
            store_id=store_id,
        )
        return predict
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
