# import stuff
from pathlib import Path
import pandas as pd

# load data from folder
folder = Path('./data/processed')

# filtered datasets with mortgage rates
sold = pd.read_csv(folder / 'wk6_sold.csv', low_memory = False)
listings = pd.read_csv(folder / 'wk6_listings.csv', low_memory = False)

def iqr(df, df_name):
    '''
    purpose: implements statistical method to identify, flag, and
    remove outliers so the data doesn't misrepresent the typical market
    '''
    fields = ['ClosePrice',
              'LivingArea',
              'DaysOnMarket']

    print(f'{df_name.upper()} dataset:')

    for field in fields:
        Q1 = df[field].quantile(0.25)
        Q3 = df[field].quantile(0.75)

        IQR = Q3 - Q1

        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR

        # flag outliers
        flagged_df = df.copy()
        flagged_df[f'{field}_outlier'] = (df[field] >= lower) & (df[field] <= upper)

        print(f'{field} after flagging outliers:')
        print('Dataset size:', flagged_df.shape)
        print('Median:', flagged_df[field].median(), '\n')

        # remove outliers
        clean_df = df[(df[field] >= lower) & (df[field] <= upper)]

        print(f'{field} after removing outliers:')
        print(f'Dataset size:', clean_df.shape)
        print('Median:', clean_df[field].median(), '\n')

        og_size = flagged_df[field].shape[0]
        new_size = clean_df[field].shape[0]

        og_median = flagged_df[field].median()
        new_median = clean_df[field].median()

        pct_removed = ((og_size - new_size) / og_size) * 100
        median_change_pct = ((og_median - new_median) / og_median) * 100

        print('Rows removed (%):', round(pct_removed, 2))
        print('Median change (%):', round(median_change_pct, 2))


    return clean_df, flagged_df

sold_no_outliers, sold_flag_outliers = iqr(sold, 'sold')
listings_no_outliers, listings_flag_outliers = iqr(listings, 'listings')

print('Saving sold without outliers...')
sold_no_outliers.to_csv('./data/processed/wk7_sold_clean.csv', index = False)
print('Saving sold with outliers...')
sold_flag_outliers.to_csv('./data/processed/wk7_sold_flagged.csv', index = False)

print('Saving listings without outliers...')
listings_no_outliers.to_csv('./data/processed/wk7_listings_clean.csv', index = False)
print('Saving listings with outliers...')
listings_flag_outliers.to_csv('./data/processed/wk7_listings_flagged.csv', index = False)

print('Datasets successfully saved.')