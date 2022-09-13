import os
import requests
from datetime import date
from .ml_models import housing_prices_model, job_trends_model
from functools import cache
from pytrends.request import TrendReq

headers = {
    "Authorization": "Bearer "
}

@cache
def get_avg_housing_increase_or_decrease(zipCode, num_years):
    url = f"https://api.bridgedataoutput.com/api/v2/zestimates_v2/zestimates?postalCode={zipCode}"
    houses = requests.get(url=url, headers=headers).json()['bundle']
    percent_diffs = []
    for house in houses:
        current_price = house['zestimate']
        address = house['address']
        historical_prices = get_historical_pricing(
            address) + [[date.today().year, current_price] if current_price else []]
        if len(historical_prices) > 2:
            modelled_prices = housing_prices_model(
                historical_prices, num_years)
            predicted_price = modelled_prices[-1][-1]
            percent_diff = (
                (predicted_price - current_price) / current_price) * 100
            percent_diffs.append(percent_diff)
        else:
            percent_diffs.append(0)
    return sum(percent_diffs) / len(percent_diffs)

def get_historical_pricing(address):
    url = f"https://api.bridgedataoutput.com/api/v2/pub/assessments?address.full='{address}'"
    historical_data = requests.get(url=url, headers=headers).json()['bundle']
    year_price_data = [[data['year'], data['marketTotalValue']]
                       for data in historical_data if data['year'] and data['marketTotalValue']]
    return sorted(year_price_data, key=lambda x: x[0])

def get_job_inc_or_dec(job_title, num_years):
    pytrend = TrendReq()
    keywords=[job_title]
    pytrend.build_payload(keywords, cat=0, timeframe='today 5-y')
    df = pytrend.interest_over_time() 
    df = df[job_title]
    df = df.reset_index()
    df = df.rename(columns={"date":"ds", job_title:"y"})
    current_value = df.values[-1][-1]
    predicted_value = job_trends_model(df, num_years)[-1][-1]
    percent_change = ((predicted_value - current_value) / current_value) * 100
    return percent_change
