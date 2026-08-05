# import stuff
from pathlib import Path
import pandas as pd
import numpy as np

# load data from folder
folder = Path('./data/processed')

# filtered datasets with mortgage rates
sold = pd.read_csv(folder / 'wk3_sold_with_rates.csv', low_memory = False)
listings = pd.read_csv(folder / 'wk3_listings_with_rates.csv', low_memory = False)

# null count summary as reference for cleaning
sold_null_summary = pd.read_csv(folder / 'wk2_sold_null_summary.csv', index_col = 0)
listings_null_summary = pd.read_csv(folder / 'wk2_listings_null_summary.csv', index_col = 0)

def load_dataset(df, df_name):
    '''purpose: ensure that datasets & their null count summaries loaded properly'''

    print(f'{df_name} dataset shape:', df.shape, '\n')
    print(df.head())

    if df_name == 'sold':
        print(f'{df_name} null summary dataset:\n', sold_null_summary.head())
    elif df_name == 'listings':
        print(f'{df_name} null summary dataset:\n', listings_null_summary.head())
    print('\n')
    
def clean_cols(df, df_name):
    '''
    purpose: 
    - convert date fields to datetime format,
    - remove unnecessary/redundant columns,
    - handle missing values appropriately,
    - ensure numeric fields are properly typed,
    - remove/flag invalid numeric values
    '''

    print(f'Cleaning {df_name.upper()} dataset...\n')
    # convert date columns to datetime format
    date_cols = ['CloseDate',
                'PurchaseContractDate',
                'ListingContractDate',
                'ContractStatusChangeDate']
    df[date_cols] = df[date_cols].apply(pd.to_datetime, errors = 'coerce')

    # check that changes have been made
    print('Check that datetime changes have been applied:')
    print(df[date_cols].dtypes, '\n')

    # check cols w >90% nulls
    if df_name == 'sold':
        flag_over_90 = sold_null_summary[sold_null_summary['null pct'] > 90].index.tolist()
    elif df_name == 'listings':
        flag_over_90 = listings_null_summary[listings_null_summary['null pct'] > 90].index.tolist()
    
    print('Columns with over 90% nulls:\n', flag_over_90, '\n')

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

    print(f'{df_name} shape after dropping columns with over 90% nulls:', df.shape)

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
        flag_over_50 = listings_null_summary[listings_null_summary['null pct'] > 50].index.tolist()

    # recall wk2-3: remove core fields from the list of cols to drop
    core_fields = ['ClosePrice', 'ListPrice', 'OriginalListPrice',
                'LivingArea', 'LotSizeAcres', 'BedroomsTotal',
                'BathroomsTotalInteger', 'DaysOnMarket', 'YearBuilt']

    for field in core_fields:
        if field in flag_over_50:
            flag_over_50.remove(field)

    print('\n', len(flag_over_50), 'columns with over 50% nulls (excl. core fields):')
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

    # remove school fields from flagged
    for field in school_fields:
        if field in flag_over_50:
            flag_over_50.remove(field)

    # remove overlapping cols from flag50
    for i in flag_over_90:
        for j in flag_over_50:
            if j in flag_over_90:
                flag_over_50.remove(j)

    # flag_over_50.sort()
    print('\n', len(flag_over_50), 'columns with over 50% nulls (excl. core fields & schools):')
    flag_over_50.remove('BuyerOfficeName')
    print(flag_over_50)

    # drop cols w >50% nulls (excl. core fields and schools)
    clean_df = df.drop(columns = flag_over_50)
    print(f'{df_name} shape after dropping:', clean_df.shape)

    # manually remove columns
    cols_to_remove = ['ListAgentFirstName',     # listagentfullname column exists
                      'ListAgentLastName',          # same as above
                      'StreetNumberNumeric',    # unhelpful for analysis
                      'ListAgentEmail',         # unhelpful for analysis
                      'PropertyType',           # filtered to residential property types
                      'LotSizeArea',            # a mix of sq ft. and acres populate this column
                      'StateOrProvince',        # filtered to only california properties
                      'ListingKeyNumeric',      # equivalent to listingkey column
                      ]

    if df_name == 'sold':
        cols_to_remove.append('MlsStatus')  # sold properties = all statuses are closed
        cols_to_remove.append('BuyerAgentFirstName')    # buyeragentmlsid column exists
        cols_to_remove.append('BuyerAgentLastName')     # same as above
    elif df_name == 'listings':
        # drop dupe cols
        dupe_cols = [col for col in clean_df.columns if col.endswith('.1')]
        for col in dupe_cols:
            cols_to_remove.append(col)

    clean_df = clean_df.drop(columns = cols_to_remove)
    print(f'\nFinal {df_name.upper()} shape after dropping columns:', clean_df.shape)
    
    return clean_df

def consistency_checks(df, df_name):
    '''
    purpose:
    - validate logical order of date fields (ListingContractDate should precede PurchaseContractDate which should precede CloseDate)
    - create boolean flag cols to mark records that violate these rules
        - listing_after_close_flag
        - purchase_after_close_flag
        - negative_timeline_flag
    - check for invalid values in numeric fields
    '''

    # flag for negative closeprice
    df['neg_closeprice_flag'] = df['ClosePrice'] <= 0
    print('# of rows with negative ClosePrice:', df[df['neg_closeprice_flag'] == True].shape[0])

    # flag for negative livingarea
    df['neg_livingarea_flag'] = df['LivingArea'] <= 0
    print('\n# of rows with negative LivingArea:', df[df['neg_livingarea_flag'] == True].shape[0])

    # flag negative DOM
    df['neg_dom_flag'] = df['DaysOnMarket'] < 0
    print('\n# of rows with negative DaysOnMarket:', df[df['neg_dom_flag'] == True].shape[0])

    if df_name == 'sold':
        # validate logical order of date fields
        invalid_rows = df[~((df['ListingContractDate'] < df['PurchaseContractDate']) & 
                            (df['PurchaseContractDate'] < df['CloseDate']))]
        
        print('\nShape of rows where date fields are out of order', invalid_rows.shape)
        print(invalid_rows[['ListingContractDate', 'PurchaseContractDate', 'CloseDate']].head())

        # create bool flag cols 
        # (correct order: list date < purchase date < close date)

        # listdate > closedate
        df['listing_after_close_flag'] = df['ListingContractDate'] > df['CloseDate']
        print('# rows where list date is after close date:', df[df['listing_after_close_flag'] == True].shape[0])

        # purchase date after close date
        df['purchase_after_close_flag'] = df['PurchaseContractDate'] > df['CloseDate']
        print('\n# rows where purchase date is after close date:', df[df['purchase_after_close_flag'] == True].shape[0])

        # violates order
        df['negative_timeline_flag'] = ~((df['ListingContractDate'] < df['PurchaseContractDate']) & 
                                        (df['PurchaseContractDate'] < df['CloseDate']))
        print('\n# rows with negative timeline:', df[df['negative_timeline_flag'] == True].shape[0])
    elif df_name == 'listings':
        df['negative_timeline_flag'] = (df['ListingContractDate'] > df['PurchaseContractDate'])
        print('\n# rows with negative timeline:', df[df['negative_timeline_flag'] == True].shape[0])


    return df

def geographic_checks(df):
    '''
    purpose:
    - flag records w missing coords (lat/lon is null)
    - flag lat = 0 or lon = 0 (sentinel null vals)
    - flag lon > 0 errors (cali coords should be negative)
    - flag out-of-state/implausible coords
    '''

    # lat/lon is null
    df['missing_coords_flag'] = (df['Latitude'].isna()) | (df['Longitude'].isna())
    print('\n# of rows with missing coordinates:', df[df['missing_coords_flag'] == True].shape[0])
    print(df[df['missing_coords_flag'] == True].head())

    # lat = 0 or lon = 0
    df['sentinel_coords_flag'] = (df['Latitude'] == 0) | (df['Longitude'] == 0)
    print('\n# of rows with sentinel null coordinates:', df[df['sentinel_coords_flag'] == True].shape[0])
    print(df[df['sentinel_coords_flag'] == True].head())

    # lon > 0
    df['pos_lon_flag'] = df['Longitude'] > 0
    print('\n# of rows with positive longitude:', df[df['pos_lon_flag'] == True].shape[0])

    # out of state (oos) coords
    df['oos_coords_flag'] = ~(df['Latitude'].between(32.0, 42.5) & df['Longitude'].between(-125.0, -113.5))
    print('\n# of rows with out-of-state coordinates:', df[df['oos_coords_flag'] == True].shape[0])

    return df

def clean_sold_rows(df):
    '''
    purpose: looks into flagged columns created from 'consistency'
    and 'geographic'-check functions for the SOLD dataset
    '''

    print('\nShape before removing negative ClosePrice & LivingArea:', df.shape)
    # remove rows with negative closeprice and livingarea
    df = df[~((df['neg_closeprice_flag'] == True) |
                    (df['neg_livingarea_flag'] == True))]
    print('Shape after removing negative ClosePrice & LivingArea:', df.shape)

    # convert negative DOM to null
    print('\n# rows with negative DOM:', df[df['neg_dom_flag'] == True]['DaysOnMarket'].shape)
    print('# nulls before conversion:', df['DaysOnMarket'].isna().sum())
    df.loc[df['neg_dom_flag'] == True, 'DaysOnMarket'] = np.nan
    # check that conversion was successful
    print('# nulls after conversion:', df['DaysOnMarket'].isna().sum(), '\n')

    # convert listing dates after close date to null
    print('\n# of rows where listing date after close date:', df[df['listing_after_close_flag'] == True].shape[0])
    print('Shape before conversion:', df.shape)
    df.loc[df['listing_after_close_flag'] == True, ['ListingContractDate', 'CloseDate']] = np.nan
    print('Shape after conversion:', df.shape)
    print('# nulls after conversion:', df[['ListingContractDate', 'CloseDate']].isna().sum(), '\n')

    # convert purchase dates after close date to null
    print('\n# of rows where purchase date after close date:', df[df['purchase_after_close_flag'] == True].shape[0])
    print('Shape before conversion:', df.shape)
    df.loc[df['purchase_after_close_flag'] == True, ['PurchaseContractDate', 'CloseDate']] = np.nan
    print('Shape after conversion:', df.shape)
    print('# nulls after conversion:', df[['PurchaseContractDate', 'CloseDate']].isna().sum(), '\n')

    # convert rows with negative timeline to null
    print('\n# of rows with negative timeline:', df[df['negative_timeline_flag'] == True].shape[0])
    print('Shape before conversion:', df.shape)
    df.loc[df['negative_timeline_flag'] == True, ['ListingContractDate', 'PurchaseContractDate', 'CloseDate']] = np.nan
    print('Shape after conversion:', df.shape)
    print('# nulls after conversion:', df[['ListingContractDate', 'PurchaseContractDate', 'CloseDate']].isna().sum(), '\n')
    
    # keep missing coordinates
    print('\n# of rows with missing coordinates:', df[df['missing_coords_flag'] == True].shape[0])

    # remove sentinel coordinates (lat/lon = 0)
    print('\n# of rows with sentinel coordinates:', df[df['sentinel_coords_flag'] == True].shape[0])
    print('Shape before removing sentinel coordinates:', df.shape)
    df = df[~(df['sentinel_coords_flag'] == True)]
    print('Shape after removing sentinel coordinates:', df.shape)

    # investigate positive longitude flag
    print('\n# of rows with positive longitude:', df[df['pos_lon_flag'] == True].shape[0])
    print('Shape before conversion:', df[df['pos_lon_flag'] == True].shape)
    df.loc[df['pos_lon_flag'] == True, ['Latitude', 'Longitude']] = np.nan
    print('Shape after conversion:', df[df['pos_lon_flag'] == True].shape)

    # investigate out-of-state coordinates
    print('\n# of rows with out-of-state coordinates:', df[df['oos_coords_flag'] == True].shape[0])
    # create mapping of zip codes to cities for out-of-state coordinates
    zip_to_city = {
        '91932': 'Imperial Beach',
        '93933': 'Marina',
        '94065': 'Redwood City',
        '92028': 'Fallbrook',
        '94904': 'Greenbrae',
        '95346': 'Mi Wuk Village',
        '92101': 'San Diego',
        '94574': 'St. Helena',
        '11217': np.nan,        # valid city but out of CA
        '63119-2447': np.nan,   # valid city but out of CA
        '88888': np.nan,        # valid city but out of CA
        '85374': np.nan         # valid city but out of CA
    }
    # apply mapping
    mask = (
        (df['oos_coords_flag']) &
        (df['City'].isna())
    )

    df.loc[mask, 'City'] = (
        df.loc[mask, 'PostalCode']
        .astype(str)
        .map(zip_to_city)
    )

    # remove non-CA rows
    print('\nShape before removing:', df.shape)
    df = df[~((df['oos_coords_flag'] == True) & (df['City'].isnull()))]
    print('Shape after removing:', df.shape)

    # remove out of state coords except cities marked 'Other'
    print('\nShape before cleaning:', df.shape)
    df = df[
        ~df['City'].isin([
            'Outside Area (Outside Ca)',
            'Outside Area (Outside U.S.) Foreign Country'
        ])
    ]
    print('Shape after cleaning:', df.shape)

    # rename cities correctly according to zipcode
    zip_to_city2 = {
        95493: 'Witter Springs',
        90032: 'Los Angeles',
        92109: 'San Diego',
        90063: 'Los Angeles',
        93603: 'Badger',
        95602: 'Auburn',
        90044: 'Los Angeles',
        90011: 'Los Angeles',
        93654: 'Reedley'
    }
    city_mask = df['City'] == 'Other'
    # apply fixes
    df.loc[city_mask, 'City'] = (
        df.loc[city_mask, 'PostalCode']
        .map(zip_to_city2)
    )

    print('\nShape before conversion:', df.shape)
    df.loc[df['oos_coords_flag'] == True, ['Latitude', 'Longitude']] = np.nan
    print('Shape after conversion:', df.shape)
    df[df['oos_coords_flag'] == True][['Latitude', 'Longitude', 'City', 'PostalCode']]

    # remove out of state rows + row with flagstaff since that's in AZ
    oos_mask = (
        df['oos_coords_flag'] &
        (df['City'].isna() |
        (df['City'] == 'Flagstaff'))
    )
    print('\nShape before removing:', df.shape)
    df = df[~oos_mask]
    print('Shape after removing:', df.shape)

    # fix palmdale zipcode
    df.loc[319267, 'PostalCode'] = 93551 # used to be 83551

    # normalize zipcodes to remove hyphens (e.g 63119-2447)
    df['PostalCode'] = (
        df['PostalCode']
        .astype(str)
        .str[:5]
    )

    # drop flagged columns that're done
    print('\nShape before removing flagged columns:', df.shape)
    df = df.drop(columns = ['neg_closeprice_flag',
                            'neg_livingarea_flag',
                            'neg_dom_flag',
                            'listing_after_close_flag',
                            'purchase_after_close_flag',
                            'negative_timeline_flag',
                            'missing_coords_flag',
                            'sentinel_coords_flag',
                            'pos_lon_flag',
                            'oos_coords_flag'])

    print('Shape after removing flagged columns:', df.shape)

    return df

def clean_listings_rows(df):
    '''
    purpose: looks into flagged columns created from 'consistency'
    and 'geographic'-check functions for the LISTINGS dataset
    '''

    # remove 0-value livingarea
    print('Shape before removing invalid LivingArea:', df.shape)
    df = df[df['neg_livingarea_flag'] == False]
    print('Shape after removing invalid LivingArea:', df.shape)

    # set negative dom values to null
    print('\n# rows with negative DOM:', df[df['neg_dom_flag'] == True]['DaysOnMarket'].shape)
    print('# nulls before conversion:', df['DaysOnMarket'].isna().sum())
    df.loc[df['neg_dom_flag'] == True, 'DaysOnMarket'] = np.nan
    print('# nulls after conversion:', df['DaysOnMarket'].isna().sum())

    # investigate negative timeline flag
    neg_timeline_mask = df[df['negative_timeline_flag'] == True]
    # turn wrong dates into null
    print('\n# rows with wrong timeline:', neg_timeline_mask[['ListingContractDate', 'PurchaseContractDate', 'DaysOnMarket']].shape)
    print('# nulls before conversion:\n', df[['ListingContractDate', 'PurchaseContractDate']].isna().sum())
    df.loc[df['negative_timeline_flag'] == True, ['ListingContractDate', 'PurchaseContractDate']] = np.nan
    print('# nulls after conversion:\n', df[['ListingContractDate', 'PurchaseContractDate']].isna().sum())

    # investigate missing coords flag
    missing_coords_mask = df[df['missing_coords_flag'] == True]
    print('\n# rows with missing coordinates:', missing_coords_mask.shape[0])

    # investigate sentinel coords
    sentinel_coords_mask = df[df['sentinel_coords_flag'] == True]
    print('\n# rows with sentinel coordinates:', sentinel_coords_mask.shape[0])
    # remove 0 lat/lon values
    print('Shape before removing:', df.shape)
    df = df[df['sentinel_coords_flag'] == False]
    print('Shape after removing:', df.shape)

    # investigate positive longitude flag
    pos_lon_mask = df[df['pos_lon_flag'] == True]
    print('\n# rows outside CA:', pos_lon_mask.shape[0])

    # set coordinate values to null
    # even though cities correspond to their zipcodes, the lat/lon aren't within CA bounds
    print('Before conversion:')
    print(df.loc[
        df['pos_lon_flag'] == True,
        ['Latitude', 'Longitude']
    ].head())

    # some coordinates seem to be misinputted, so we can flip longitude sign
    df.loc[
        df['pos_lon_flag'] == True,
        'Longitude'
    ] *= -1
    print('\nAfter conversion:')
    print(df.loc[
        df['pos_lon_flag'] == True,
        ['Latitude', 'Longitude']
    ].head())

    print('Before reflagging:')
    print(df['pos_lon_flag'].value_counts())
    df['pos_lon_flag'] = df['Longitude'] > 0
    print('\nAfter reflagging:')
    print(df['pos_lon_flag'].value_counts())

    # also reflag oos coords
    print('Before reflagging:')
    print(df['oos_coords_flag'].value_counts())
    df['oos_coords_flag'] = ~(df['Latitude'].between(32.0, 42.5) & df['Longitude'].between(-125.0, -113.5))
    print('\nAfter reflagging:')
    print(df['oos_coords_flag'].value_counts())

    # look into out of state coords
    oos_mask = df[df['oos_coords_flag'] == True]
    print('\n# rows with out of state/implausible coordinates:', oos_mask.shape[0])

    # remove non-cali coords via lat/lon
    noncali_coords_mask = (
            df['oos_coords_flag'] == True &
            ~(
                df['Latitude'].notnull() &
                df['Longitude'].notnull()
            )
            )
    print('\nShape before removing:', df.shape)
    print('Shape of oos_cords_flag before removal:', df['oos_coords_flag'].shape)
    df = df[noncali_coords_mask]
    print('Shape after removing:', df.shape)
    print('Shape of oos_cords_flag after removal:', df['oos_coords_flag'].shape)

    # remove non-cali via postal code
    noncali_postal_mask = (
        df['oos_coords_flag'] &
        ~df['PostalCode'].astype(str).str.startswith('9')
    )
    print("\nRows to remove:", noncali_postal_mask.sum())
    print('Shape before removing:', df.shape)
    print('Shape of oos_cords_flag before removal:', df['oos_coords_flag'].shape)
    df = df[~noncali_postal_mask]
    print('Shape after removing:', df.shape)
    print('Shape of oos_cords_flag after removal:', df['oos_coords_flag'].shape)

    # convert nan cities according to zipcode
    zip_to_city = {
        '92061': 'Pauma Valley',
        '94065': 'Redwood City',
        '95004': 'Aromas',
        '93933': 'Marina',
        '95670': 'Rancho Cordova',
        '92111': 'San Diego',
        '95703': 'Auburn',
        '91932': 'Imperial Beach',
        '94074': 'San Gregorio',
        '93908': 'Salinas',
        '91326': 'Porter Ranch',
        '91962': 'Pine Valley',
        '95419': 'Camp Meeker',
        '94904': 'Greenbrae',
        '92240': 'Desert Hot Springs',
        '91906': 'Campo',
        '94574': 'Saint Helena',
        '95497': 'The Sea Ranch',
        '95002': 'Alviso',
        '92128': 'San Diego',
        '94028': 'Portola Valley',
        '96022': 'Cottonwood',
        '90710': 'Harbor City',
        '92129': 'San Diego',
        '96137': 'Westwood',
        '92109': 'San Diego',
        '93291': 'Visalia',
        '95023': 'Hollister',
        '99999': np.nan,  # invalid zipcode
        '94516': 'Crockett',
        '95635': 'Greenwood',
        '95076': 'Watsonville',
        '95346': 'Mi Wuk Village',
        '92037': 'La Jolla',
        '92549': 'Idyllwild',
        '92676': 'Silverado',
        '93266': 'Stratford',
        '95628': 'Fair Oaks',
        '95664': 'Pilot Hill',
        '91411': 'Van Nuys',
        '95006': 'Boulder Creek',
        '92123': 'San Diego',
        '94062': 'Redwood City',
        '93222': 'Frazier Park',
        '94520': 'Concord',
        '92075': 'Solana Beach',
        '93015': 'Fillmore',
        '96136': 'Susanville',
        '95246': 'Linden',
        '95545': 'Honeydew',
        '95961': 'Olivehurst',
        '95614': 'Cool',
        '95364': 'Stevinson',
        '96048': 'Junction City',
        '93608': 'Cantua Creek',
        '94303': 'Palo Alto',
        '95385': 'Winton',
        '92024': 'Encinitas',
        '92028': 'Fallbrook',
        '96146': 'Olympic Valley',
        '95305': 'Coulterville',
        '95314': 'Cressey'
    }
    # normalize zipcodes to remove the hyphens
    df['PostalCode'] = (
        df['PostalCode']
        .astype(str)
        .str[:5]
    )
    # map zipcode to the correct city
    df['City'] = (
        df['City']
        .fillna(
            df['PostalCode'].astype(str).map(zip_to_city)
        )
    )
    # confirm changes were made
    df[df['oos_coords_flag'] == True][['Latitude', 'Longitude', 'City', 'PostalCode']].isna().sum()

    # remove rows with 99999 postal code
    print('\nShape before removing:', df.shape)
    print('Shape of oos_cords_flag before removal:', df['oos_coords_flag'].shape)
    df = df[df['PostalCode'] != '99999']
    print('Shape after removing:', df.shape)
    print('Shape of oos_cords_flag after removal:', df['oos_coords_flag'].shape)

    # double check that changes were made
    df[df['oos_coords_flag'] == True][['City']].isna().sum()

    # drop flagged columns
    print('\nShape before removing flagged columns:', df.shape)
    df = df.drop(columns = ['neg_livingarea_flag',
                            'neg_dom_flag',
                            'negative_timeline_flag',
                            'missing_coords_flag',
                            'sentinel_coords_flag',
                            'pos_lon_flag',
                            'oos_coords_flag'])
    print('Shape after removing flagged columns:', df.shape)

    return df

def cleaning_pipeline(df, df_name):
    print('LOADING DATASET...\n')
    load_dataset(df, df_name)

    print('STARTING CLEANING...\n')
    clean_df = clean_cols(df, df_name)

    print('PERFORMING CONSISTENCY CHECKS...\n')
    clean_df = consistency_checks(clean_df, df_name)

    print('PERFORMING GEOGRAPHIC CHECKS...\n')
    clean_df = geographic_checks(clean_df)

    print('CLEANING ROWS...\n')
    if df_name == 'sold':
        clean_df = clean_sold_rows(clean_df)
    elif df_name == 'listings':
        clean_df = clean_listings_rows(clean_df)

    # save new df as csv
    print('\n\nSaving dataframe to csv...')
    clean_df.to_csv(f'./data/processed/wk4_5_{df_name}_clean.csv', index = False)
    print('Successfully saved')

cleaning_pipeline(sold, 'sold')
cleaning_pipeline(listings, 'listings')