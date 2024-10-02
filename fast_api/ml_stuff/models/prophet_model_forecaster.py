import datetime
import pandas as pd

def sales_forecast(target_date: datetime.date, m):
    target_date = pd.to_datetime(target_date)
    target_date_end = target_date + pd.Timedelta(days=7)
    last_date = pd.to_datetime("2015-04-18")
    days_to_forecast = (target_date_end - last_date).days

    # Create a future DataFrame
    future = m.make_future_dataframe(
        periods=days_to_forecast, freq="D"
    )  
    forecast = m.predict(future)
    forecast_api = forecast[["ds", "yhat"]].tail(7)
    forecast_api["ds"] = forecast_api["ds"].dt.date
    forecast_dict = forecast_api.set_index("ds")["yhat"].to_dict()
    return forecast_dict
