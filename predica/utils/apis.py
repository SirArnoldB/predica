
import os
import requests
from datetime import date
from .ml_models import housing_prices_model
from functools import cache

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
    for x in percent_diffs:
        print(x)
        print()
    return sum(percent_diffs) / len(percent_diffs)


def get_historical_pricing(address):
    url = f"https://api.bridgedataoutput.com/api/v2/pub/assessments?address.full='{address}'"
    historical_data = requests.get(url=url, headers=headers).json()['bundle']
    year_price_data = [[data['year'], data['marketTotalValue']]
                       for data in historical_data if data['year'] and data['marketTotalValue']]
    return sorted(year_price_data, key=lambda x: x[0])

'''

-104.2156624996533

-17.16081361779702

121.65559509410144

44.6159174068799

89.9804896798872

120.17654548088213

57.37183337153448

-61.58070900931516

88.01442178835933

59.263045906828495
'''
