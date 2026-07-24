# import stuff
from pathlib import Path
import pandas as pd
import numpy as np
import geopandas as gpd

# load data from folder
folder = Path('./data/processed')

# filtered datasets with mortgage rates
sold = pd.read_csv(folder / 'sold_clean.csv', low_memory = False)
listings = pd.read_csv(folder / 'listings_clean.csv', low_memory = False)

print(sold.head())
print(listings.head())

def ft_eng(df, df_name):
    ''' 
    purpose: create key metrics using existing columns
    and add school districts using properties' lat/lon values
    '''

    # measures negotiation strength
    df['price_ratio'] = df['ClosePrice'] / df['OriginalListPrice']

    # normalizes price across sizes
    df['price_per_sqft'] = df['ClosePrice'] / df['LivingArea']

    # enables time-series analysis
    df['year'] = df['CloseDate'].dt.year
    df['month'] = df['CloseDate'].dt.month
    # df['YrMo'] = df['CloseDate'].dt.to_period('M')

    # captures full price reduction history
    df['close_to_original_list_ratio'] = df['ClosePrice'] / df['OriginalListPrice']

    # measures time from listing to accepted offer
    df['listing_to_contract_days'] = df['PurchaseContractDate'] - df['ListingContractDate']

    # measures time from purchase date to close date
    df['contract_to_close_days'] = df['CloseDate'] - df['PurchaseContractDate']

    # add school districts


def segment_analysis(df, df_name):
    ''' 
    purpose: generate summary statistics of key dimensions
    to uncover market patterns
    '''

def pipeline(df, df_name):
    ''' 
    purpose: run feature engineering function and segment
    analysis in one go instead of running each separately
    '''
    ft_eng(df, df_name)
    segment_analysis(df, df_name)

# pipeline(sold, 'sold')
# pipeline(listings, 'listings')