# import stuff
import pandas as pd
from pathlib import Path # to load sold & listings datasets

# hide api stuff
from dotenv import load_dotenv
import os

load_dotenv()

# fetch mortgage rate data from FRED
url = os.getenv('FRED_URL')

mortgage = pd.read_csv(url, parse_dates = ['observation_date'])
mortgage.columns = ['date', 'rate_30yr_fixed']

# resample weekly rates to monthly avgs
mortgage['year_month'] = mortgage['date'].dt.to_period('M')

mortgage_monthly = (
    mortgage.groupby('year_month')['rate_30yr_fixed']
    .mean()
    .reset_index()
)

# create matching year_month key on MLS datasets
# load in sold & listings dataset from wk2
folder = Path('./data')

listings = pd.read_csv(folder / 'listings.csv')
sold = pd.read_csv(folder / 'sold.csv')

# sold dataset: key off closedate
sold['year_month'] = pd.to_datetime(sold['CloseDate']).dt.to_period('M')

# listings dataset: key off listingcontractdate
listings['year_month'] = pd.to_datetime(
    listings['ListingContractDate']
).dt.to_period('M')

# merge
sold_with_rates = sold.merge(mortgage_monthly, on = 'year_month', how = 'left')
listings_with_rates = listings.merge(mortgage_monthly, on = 'year_month', how = 'left')

# validate merge
print('Null values in sold_with_rates:', sold_with_rates['rate_30yr_fixed'].isnull().sum())
print('Null values in listings_with_rates:', listings_with_rates['rate_30yr_fixed'].isnull().sum())

# preview
print(sold_with_rates[
    ['CloseDate', 'year_month', 'ClosePrice', 'rate_30yr_fixed']
].head())

# save merged datasets
sold_with_rates.to_csv('./data/sold_with_rates.csv', index = False)
listings_with_rates.to_csv('./data/listings_with_rates.csv', index = False)