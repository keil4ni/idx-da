'''
WK4-5 DELIVERABLE
- document every xformation made & why
- include:
    - before/after counts
    - dtype confirmations
    - date consistency flag counts
    - geographic data quality summary noting invalid coordinate records
'''

# import stuff
from pathlib import Path
import pandas as pd
# import matplotlib.pyplot as plt

# load data from folder
folder = Path('./data')

# filtered datasets with mortgage rates
sold = pd.read_csv(folder / 'sold_with_rates.csv', low_memory = False)
listings = pd.read_csv(folder / 'listings_with_rates.csv', low_memory = False)

# null count summary as reference for cleaning
sold_null_summary = pd.read_csv(folder / 'sold_null_summary.csv', index_col = 0)
listings_null_summary = pd.read_csv(folder / 'listings_null_summary.csv', index_col = 0)

def load_dataset(df, df_name):
    '''purpose: ensure that datasets & their null count summaries loaded properly'''

    print(f'{df_name} dataset shape:', df.shape)
    print(df.head())

    if df_name == 'sold':
        print(f'{df_name} null summary dataset:\n', sold_null_summary)
    elif df_name == 'listings':
        print(f'{df_name} null summary dataset:\n', listings_null_summary)
    
def clean_dataset(df, df_name):
    '''
    purpose: 
    - convert date fields to datetime format,
    - remove unnecessary/redundant columns,
    - handle missing values appropriately,
    - ensure numeric fields are properly typed,
    - remove/flag invalid numeric values
    '''

    print(f'Cleaning {df_name} dataset...')
    # convert date columns to datetime format
    date_cols = ['CloseDate',
                'PurchaseContractDate',
                'ListingContractDate',
                'ContractStatusChangeDate']
    df[date_cols] = df[date_cols].apply(pd.to_datetime, errors = 'coerce')

    # check that changes have been made
    print('Check that datetime changes have been applied:')
    print(df[date_cols].dtypes)

    # check cols w >90% nulls
    if df_name == 'sold':
        flag_over_90 = sold_null_summary[sold_null_summary['null pct'] > 90].index.tolist()
    elif df_name == 'listings':
        flag_over_90 = listings_null_summary[listings_null_summary['null pct'] > 90].index.tolist()
    
    # flag_over_90.sort()
    print('Columns with over 90% nulls:\n', flag_over_90)

    '''
    from the real_estate_primer.pdf, our key data fields are:
    listingkey, listingcontractdate, listprice,
    closeprice, purchasecontractdate, closedate,
    livingarea, bedroomstotal, bathroomstotalinteger,
    latitude, longitude, unparsedaddress

    since the flagged columns do not include any of these key fields, we can remove them

    '''

    # drop cols w >90% nulls
    df = df.drop(columns = flag_over_90)

    print(f'{df_name} shape after dropping:', df.shape)
    print(df.head())

    '''
    we can also consider dropping columns with over 50% nulls for more meaningful analyses,
    but we will still make sure none of the flagged columns involve key data fields. from
    the week 2-3 deliverables, we were given a list of key numeric fields (in which I will
    define as core_fields), so we should make sure those are not flagged either
    '''

    # consider dropping cols w >50% nulls
    if df_name == 'sold':
        flag_over_50 = sold_null_summary[sold_null_summary['null pct'] > 50].index.tolist()
    elif df_name == 'listings':
        flag_over_50 == listings_null_summary[listings_null_summary['null pct'] > 50].index.tolist()

    # remove core fields from the list of cols to drop
    core_fields = ['ClosePrice', 'ListPrice', 'OriginalListPrice',
                'LivingArea', 'LotSizeAcres', 'BedroomsTotal',
                'BathroomsTotalInteger', 'DaysOnMarket', 'YearBuilt']

    for field in core_fields:
        if field in flag_over_50:
            flag_over_50.remove(field)

    # flag_over_50.sort()
    print(len(flag_over_50), 'columns with over 50% nulls (excl. core fields):')
    print(flag_over_50)

    '''
    in week 6, we will be feature engineering using existing columns and also adding school 
    districts using properties' latitude and longitude values, so we will exclude removing 
    schools and school districts in case we end up populating them in future deliverables
    '''

    # remove schools and school districts from flagged cols
    school_fields = ['ElementarySchool',
                    'ElementarySchoolDistrict',
                    'MiddleOrJuniorSchool',
                    'MiddleOrJuniorSchoolDistrict',
                    'HighSchool']

    for field in school_fields:
        if field in flag_over_50:
            flag_over_50.remove(field)

    for i in flag_over_90:
        for j in flag_over_50:
            if j in flag_over_90:
                flag_over_50.remove(j)

    # flag_over_50.sort()
    print(len(flag_over_50), 'columns with over 50% nulls (excl. core fields):')
    print(flag_over_50)

    # drop cols w >50% nulls (excl. core fields and schools)
    clean_df = df.drop(columns = flag_over_50)
    print('Sold shape after dropping:', clean_df.shape)

    print(clean_df.head())

    # take a look at remaining columns to determine what else to remove
    print(sorted(clean_df.columns))

    cols_to_remove = ['ListAgentFirstName',     # listagentfullname column exists
                      'ListAgentLastName',          # same as above
                      'StreetNumberNumeric',    # unhelpful for analysis
                      'ListAgentEmail',         # unhelpful for analysis
                      'PropertyType',           # filtered to residential property types
                      'LotSizeArea',            # a mix of sq ft. and acres populate this column
                      'StateOrProvince',         # filtered to only california properties
                      'ListingKeyNumeric',      # equivalent to listingkey column
                      'BuyerAgentFirstName',    # buyeragentmlsid column exists
                      'BuyerAgentLastName',         # same as above
                      ]

    clean_df = clean_df.drop(columns = cols_to_remove)
    if df_name == 'sold':
        clean_df = clean_df.drop(columns = 'MlsStatus')
        # sold properties means all mls statuses are closed

    print('Shape of df after dropping columns:', clean_df.shape)
    print(clean_df.head())

def consistency_checks(df, df_name):
    '''
    purpose:
    - validate logical order of date fields (ListingContractDate should precede PurchaseContractDate which should precede CloseDate)
    - create boolean flag cols to mark records that violate these rules
        - listing_after_close_flag
        - purchase_after_close_flag
        - negative_timeline_flag
    '''
    print('Starting consistency checks...')
    # validate logical order of date fields
    invalid_rows = df[~((df['ListingContractDate'] < df['PurchaseContractDate']) & 
                        (df['PurchaseContractDate'] < df['CloseDate']))]
    
    print('Shape of rows where date fields are out of order', invalid_rows.shape)
    print(invalid_rows[['ListingContractDate', 'PurchaseContractDate', 'CloseDate']].head())

    # create bool flag cols 
    # (correct order: list date < purchase date < close date)

    # listdate > closedate
    df['listing_after_close_flag'] = df['ListingContractDate'] > df['CloseDate']
    # purchase date after close date
    df['purchase_after_close_flag'] = df['PurchaseContractDate'] > df['CloseDate']
    # violates order
    df['negative_timeline_flag'] = ~((df['ListingContractDate'] < df['PurchaseContractDate']) & 
                                    (df['PurchaseContractDate'] < df['CloseDate']))

    # check that these columns were made
    df[['listing_after_close_flag', 'purchase_after_close_flag', 'negative_timeline_flag']].head()

def geographic_checks(df, df_name):
    '''
    purpose:
    - flag records w missing coords (lat/lon is null)
    - flag lat = 0 or lon = 0 (sentinel null vals)
    - flag lon > 0 errors (cali coords should be negative)
    - flag out-of-state/implausible coords
    '''

    # lat/lon is null
    df['missing_coords_flag'] = (df['Latitude'].isna()) | (df['Longitude'].isna())

    print(df[df['missing_coords_flag'] == True].shape)
    print(df[df['missing_coords_flag'] == True].head())

    # lat = 0 or lon = 0
    df['sentinel_coords_flag'] = (df['Latitude'] == 0) | (df['Longitude'] == 0)

    print(df[df['sentinel_coords_flag'] == True].shape)
    print(df[df['sentinel_coords_flag'] == True].head())

    # lon > 0
    df['pos_lon_flag'] = df['Longitude'] > 0
    # output should be 0 since i already filtered out non-cali coordinates in cleaning


def cleaning_pipeline(df, df_name):
    load_dataset(df)
    clean_dataset(df, df_name)
    consistency_checks(df, df_name)
    geographic_checks(df, df_name)

    # if df_name == 'sold':
    #     clean_df.to_csv(f'./data/sold_clean.csv', index = False)
    # if df_name == 'listings':
    #     clean_df.to_csv(f'./data/listings_clean.csv', index = False)

# clean_dataset(sold, 'sold')