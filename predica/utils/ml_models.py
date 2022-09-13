import numpy as np
import pandas as pd
from fbprophet import Prophet

def housing_prices_model(data, num_years):
    model = Prophet()
    data = np.array(data)
    df = pd.DataFrame(data, columns=['ds', 'y'])
    df['ds'] = pd.to_datetime(df.ds, format='%Y')
    model.fit(df)
    future = model.make_future_dataframe(num_years, freq='Y')
    forecast = model.predict(future)
    #forecast = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
    return forecast.values.tolist()

def job_trends_model(df, num_years):
    model = Prophet()
    model.fit(df)
    future = model.make_future_dataframe(num_years, freq='Y')
    forecast = model.predict(future)
    forecast = forecast[['ds', 'yhat']]
    return forecast.values.tolist()
