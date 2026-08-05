# import stuff
from pathlib import Path
import pandas as pd
import geopandas as gpd

# load data from folder
folder = Path('./data/processed')

# filtered datasets with mortgage rates
sold = pd.read_csv(folder / 'wk4_5_sold_clean.csv', low_memory = False)
listings = pd.read_csv(folder / 'wk4_5_listings_clean.csv', low_memory = False)

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

    # i know i converted date fields to datetime but it didnt get saved as datetime
    date_cols = ['CloseDate',
                'PurchaseContractDate',
                'ListingContractDate',
                'ContractStatusChangeDate']
    if df_name == 'listings':
        date_cols.remove('CloseDate')

    df[date_cols] = df[date_cols].apply(pd.to_datetime, errors = 'coerce')

    # enables time-series analysis
    if df_name == 'sold':
        df['year'] = df['CloseDate'].dt.year
        df['month'] = df['CloseDate'].dt.month
        # we already have this column called year_month in the dataset
        # df['YrMo'] = df['CloseDate'].dt.to_period('M')

        # measures time from purchase date to close date
        df['contract_to_close_days'] = df['CloseDate'] - df['PurchaseContractDate']

        # captures full price reduction history
        df['close_to_original_list_ratio'] = df['ClosePrice'] / df['OriginalListPrice']

        # measures time from listing to accepted offer
        df['listing_to_contract_days'] = df['PurchaseContractDate'] - df['ListingContractDate']

        # check that engineered columns were created
        print(
            df[['price_ratio',
                'price_per_sqft',
                'year',
                'month',
                'close_to_original_list_ratio',
                'listing_to_contract_days',
                'contract_to_close_days'
                ]].head()
        )
    elif df_name == 'listings':
        # listings doesnt have a closedate col so we cant ft eng the other 4 we made for sold
        df['close_to_original_list_ratio'] = df['ClosePrice'] / df['OriginalListPrice']
        df['listing_to_contract_days'] = df['PurchaseContractDate'] - df['ListingContractDate']

        print(
            df[['close_to_original_list_ratio',
                'listing_to_contract_days'
                ]].head()
        )


    return df

def add_school_districts(df):
    ''' 
    purpose: add school districts using the properties'
    latitude/longitude values
    '''
    school_gdf = gpd.read_file('./data/school_districts.geojson')
    # filter to only include unified school districts
    filtered_school_gdf = school_gdf[school_gdf['DistrictType'] == 'Unified']
    # only add DistrictName col & geometry for merging
    filtered_school_gdf = filtered_school_gdf[['DistrictName', 'geometry']]

    # convert each property's lat/lon into geographic point
    df_gdf = gpd.GeoDataFrame(
        df,
        geometry = gpd.points_from_xy(df['Longitude'], df['Latitude']),
        crs = 'EPSG:4326'   # coordinate reference system
    )

    # standardize coord systems so they match otherwise you get a crs mismatch error
    if df_gdf.crs != school_gdf.crs:
        df_gdf = df_gdf.to_crs(school_gdf.crs)

    # spatial join to determine which unified school district polygon contains each property
    merged_df = gpd.sjoin(
        df_gdf,
        filtered_school_gdf,
        how = 'left',
        predicate = 'within'
    )

    return merged_df


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
        print(df[metric].describe(), '\n')


def pipeline(df, df_name):
    ''' 
    purpose: run feature engineering function and segment
    analysis in one go instead of running each separately
    '''
    clean_df = ft_eng(df, df_name)
    clean_df = add_school_districts(clean_df)
    segment_analysis(clean_df, df_name)

    # ensure ft eng was performed and school districts were added
    new_cols = ['price_ratio',
                'price_per_sqft',
                'year',
                'month',
                'close_to_original_list_ratio',
                'listing_to_contract_days',
                'contract_to_close_days',
                'DistrictName',
                'geometry']
    if df_name == 'listings':
        new_cols.remove('year')
        new_cols.remove('month')
        new_cols.remove('contract_to_close_days')
    
    print(clean_df[new_cols].head())

    print('Shape before removing school columns:', clean_df.shape)
    # remove school columns
    clean_df = clean_df.drop(columns = ['ElementarySchool',
                                        'MiddleOrJuniorSchool',
                                        'HighSchool',
                                        'HighSchoolDistrict'])
    print('Shape after removing school columns:', clean_df.shape)

    # save filtered dataset as new csv
    print(f'Saving {df_name} dataset to csv...')
    clean_df.to_csv(f'./data/processed/wk6_{df_name}.csv', index = False)

pipeline(sold, 'sold')
pipeline(listings, 'listings')