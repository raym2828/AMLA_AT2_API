# Import the necessary libraries
import datetime
import xgboost as xgb
import pandas as pd
import numpy as np

def sales_predict(
    df_calendar_events: pd.DataFrame,
    category_mappings,
    model,
    target_date: datetime.date,
    item_id,
    store_id,
):
    # Convert the input data to df
    data = {"date": [target_date], "item_id": [item_id], "store_id": [store_id]}
    df = pd.DataFrame(data)
    df["date"] = pd.to_datetime(df["date"])

    # Split the item_id to get the dept_id and cat_id
    df["dept_id"] = df["item_id"].apply(lambda x: "_".join(x.split("_")[:2]))
    df["cat_id"] = df["item_id"].apply(lambda x: x.split("_")[0])

    # Split the store_id to get the state_id
    df["state_id"] = df["store_id"].apply(lambda x: x.split("_")[0])

    # Add calendar events and to the inputs
    df = pd.merge(df, df_calendar_events, on="date", how="left").fillna("N")

    # Turn the categories columns into category data encoded using the same mappings as the training
    category_columns = ["item_id","dept_id","cat_id","store_id","state_id","event_name","event_type"]

    # Apply the mappings to the category columns
    for col in category_columns:
        df[col] = df[col].astype("category").cat.set_categories(category_mappings[col])

    # Convert the date to a datetime object then into integer
    df["date"] = pd.to_datetime(df["date"]).astype(int)
    df = df[["item_id","dept_id","cat_id","store_id","state_id","date","event_name","event_type"]]
    
    # Turn df into a DMatrix
    dmatrix = xgb.DMatrix(df, enable_categorical=True)

    # Make predictions
    predictions = model.predict(dmatrix, iteration_range=(0, model.best_iteration + 1))

    # # Ensure no values are less than zero
    predictions_zero_bound = np.maximum(predictions, 0)

    prediction = float(predictions_zero_bound[0])

    return prediction
