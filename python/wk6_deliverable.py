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

def ft_eng(df):
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

    # check that engineered columns were created
    print(
        df['price_ratio',
           'price_per_sqft',
           'year',
           'month',
           'close_to_original_list_ratio',
           'listing_to_contract_days',
           'contract_to_close_days'
           'DistrictName'
           ].head()
    )

def add_school_districts(df):
    ''' 
    purpose: add school districts using the properties'
    latitude/longitude values
    '''
    gdf = gpd.read_file('./data/school_districts.geojson')

    # filter to only include unified school districts
    filtered_gdf = gdf[gdf['DistrictType'] == 'Unified']

    # convert each property's lat/lon into geographic point

    # spatial join to determine which unified school district polygon contains each property

    # add DistrictName as new dataset column


def segment_analysis(df, df_name):
    ''' 
    purpose: generate summary statistics of key dimensions
    to uncover market patterns
    '''

    metrics = ['PropertySubType',
               'CountyOrParish',
               'MLSAreaMajor',
               'ListOfficeName',
               'BuyerOfficeName']

    print(f'{df_name} DATASET')

    for metric in metrics:
        print(f'Summary statistics for {metric}:')
        print(df[metric].describe())


def pipeline(df, df_name):
    ''' 
    purpose: run feature engineering function and segment
    analysis in one go instead of running each separately
    '''
    ft_eng(df)
    clean_df = add_school_districts(df)
    segment_analysis(clean_df, df_name)

    return clean_df

# sold_clean = pipeline(sold, 'sold')
# listings_clean = pipeline(listings, 'listings')

# sold_clean.to_csv('./data/processed/wk6_sold_clean.csv')
# listings_clean.to_csv('./data/processed/wk6_listings_clean.csv')