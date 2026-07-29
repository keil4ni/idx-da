# import stuff
from pathlib import Path
import pandas as pd

# load data from folder
folder = Path('./data/processed')

# filtered datasets with mortgage rates
sold = pd.read_csv(folder / 'wk6_sold.csv', low_memory = False)
listings = pd.read_csv(folder / 'wk6_listings.csv', low_memory = False)

print(sold.head())
print(listings.head())

def iqr(df):
    '''
    purpose: implements statistical method to identify, flag, and
    remove outliers so the data doesn't misrepresent the typical market
    '''
    fields = ['ClosePrice',
              'LivingArea',
              'DaysOnMarket']

    for field in fields:
        Q1 = df[field].quantile(0.25)
        Q3 = df[field].quantile(0.75)

        IQR = Q3 - Q1

        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR

        # flag outliers
        flagged_df = df.copy()
        flagged_df[f'{field}_outlier'] = (df[field] >= lower) & (df[field] <= upper)

        # remove outliers
        clean_df = df[(df[field] >= lower) & (df[field] <= upper)]


    return clean_df, flagged_df

sold_no_outliers, sold_flag_outliers = iqr(sold)
listings_no_outliers, listings_flag_outliers = iqr(listings)

print('Saving sold without outliers...')
sold_no_outliers.to_csv('./data/processed/wk7_sold_clean.csv', index = False)
print('Saving sold with outliers...')
sold_flag_outliers.to_csv('./data/processed/wk7_sold_flagged.csv', index = False)

print('Saving listings without outliers...')
listings_no_outliers.to_csv('./data/processed/wk7_listings_clean.csv', index = False)
print('Saving listings with outliers...')
listings_flag_outliers.to_csv('./data/processed/wk7_listings_flagged.csv', index = False)


'''
(ClosePrice, LivingArea, DaysOnMarket).
Add outlier flag columns rather than deleting 
records outright. Save both a full flagged dataset and a clean
filtered dataset. Include a written comparison of dataset size 
and median values before and after filtering.
'''