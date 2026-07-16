# import stuff
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

# load data from folder
folder = Path('./data')

# filtered dataset
listings = pd.read_csv(folder / 'listings.csv', low_memory = False)
sold = pd.read_csv(folder / 'sold.csv', low_memory = False)

# unfiltered dataset, needed for eda 
raw_listings = pd.read_csv(folder / 'unfiltered_listings.csv', low_memory = False)
raw_sold = pd.read_csv(folder / 'unfiltered_sold.csv', low_memory = False)

def dataset_understanding(df, df_name):
    '''
    purpose: checks columns, data types, shape, head;
             checks property categories,
             validates completeness
    '''
    print(f'{df_name} dataset shape:', df.shape)
    print(f'{df_name} dataset columns:', df.columns)
    print(f'{df_name} data types:', df.dtypes)
    print(f'{df_name} dataset head:', df.head())

def missing_val_analysis(df, df_name):
    '''
    purpose: creates null-count summary table,
             flags columns with >50% nulls,
             determine which columns to drop or retain
    '''

    # null-count summary table
    null_ct = df.isnull().sum()
    null_pct = df.isnull().mean() * 100

    null_summary = pd.DataFrame({
        'null ct': null_ct,
        'null pct': null_pct
    })

    print((null_summary.sort_values(by = 'null pct', ascending = False).head(10)))

    # save null summary table to csv based on dataset name
    if df_name == 'sold':
        null_summary.to_csv('./data/sold_null_summary.csv', index = True)
    elif df_name == 'listings':
        null_summary.to_csv('./data/listings_null_summary.csv', index = True)


    # find cols w >50% nulls
    over50 = null_summary[null_summary['null pct'] > 50]
    print(f'{df_name} dataset cols w >50% nulls:', over50.shape[0])

    flag_over50 = over50.index.tolist()
    # print(flag_over50)

    # exclude core fields from flagged list if there are any
    core_fields = ['ClosePrice', 'ListPrice', 'OriginalListPrice',
                   'LivingArea', 'LotSizeAcres', 'BedroomsTotal',
                   'BathroomsTotalInteger', 'DaysOnMarket', 'YearBuilt']
    
    for field in core_fields:
        if field in flag_over50:
            flag_over50.remove(field)

    # check if any flagged cols were removed
    print(f'{df_name} dataset flagged cols after removing core fields:', len(flag_over50))

def numeric_distrib_review(df, df_name):
    '''
    purpose: review numeric distribution of key fields using .describe(),
             data viz (histograms, boxplots, percentile summaries),
             identify extreme outliers
    '''
    numeric_fields = ['ClosePrice', 'ListPrice', 'OriginalListPrice', 
                  'LivingArea', 'LotSizeAcres', 'BedroomsTotal', 
                  'BathroomsTotalInteger', 'DaysOnMarket', 'YearBuilt']

    summary = df[numeric_fields].describe()
    print(summary)

    # find outliers
    outliers = []
    for field in numeric_fields:
        # focus on one column at a time, convert to numeric and drop nulls
        col = pd.to_numeric(df[field], errors = 'coerce').dropna()

        # find lower, upper bounds and IQR
        q1 = col.quantile(0.25)
        q3 = col.quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr

        low_outliers = int((col < lower_bound).sum())
        high_outliers = int((col > upper_bound).sum())

        outliers.append({
            'field': field,
            'min': col.min(),
            'max': col.max(),
            'lower_bound': lower_bound,
            'upper_bound': upper_bound,
            'low_outlier_ct': low_outliers,
            'high_outlier_ct': high_outliers,
            'total_outlier_ct': low_outliers + high_outliers,
            'outlier_pct': round((low_outliers + high_outliers) / len(col) * 100, 2)
        })

    outlier_df = pd.DataFrame(outliers)
    if df_name == 'sold':
        outlier_df.to_csv('./data/sold_outliers.csv', index = False)
    elif df_name == 'listings':
        outlier_df.to_csv('./data/listings_outliers.csv', index = False)

    # generate visualizations for each numeric field WITHOUT outliers
    for col in ['ClosePrice', 'LivingArea', 'DaysOnMarket']:
        plt.figure(figsize=(12, 4))
        
        # filter out outliers
        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        filtered_col = df[(df[col] >= lower_bound) & (df[col] <= upper_bound)][col]
        
        # histogram
        plt.subplot(1, 3, 1)
        plt.hist(filtered_col.dropna())
        plt.title(f'{col} Histogram (No Outliers)')
        plt.xlabel(col)
        plt.ylabel('Frequency')
        
        # boxplot
        plt.subplot(1, 3, 2)
        plt.boxplot(filtered_col.dropna())
        plt.title(f'{col} Boxplot (No Outliers)')
        plt.ylabel(col)

        # percentile summary
        plt.subplot(1, 3, 3)
        percentiles = [25, 50, 75]
        vals = filtered_col.quantile([p/100 for p in percentiles])
        plt.bar([f'{p}%' for p in percentiles], vals)
        plt.title(f'{col} Percentile Summary (No Outliers)')
        plt.ylabel(col)

        plt.savefig(f'./figs/wk2_{df_name}_{col}_viz.png')
        
        plt.tight_layout()
        plt.show()

def eda_pipeline(df, df_name):
    '''
    purpose: runs the three eda functions in sequence for a given dataset
    '''
    dataset_understanding(df, df_name)
    missing_val_analysis(df, df_name)
    numeric_distrib_review(df, df_name)

    # residential vs other property type share
    if df_name == 'sold':
        property_pct = round(raw_sold['PropertyType'].value_counts(normalize = True) * 100, 2)
        print(property_pct)
    elif df_name == 'listings':
        property_pct = round(raw_listings['PropertyType'].value_counts(normalize = True) * 100, 2)
        print(property_pct)

    # median vs average close prices
    print('Median close price:', round(df['ClosePrice'].median(), 2))
    print('Average close price:', round(df['ClosePrice'].mean(), 2))

    # days on market distribution
    df['DaysOnMarket'].describe()

    # % of homes sold above vs below list price
    above_list_price_pct = round((df[df['ClosePrice'] > df['ListPrice']].shape[0] / df.shape[0]) * 100, 2)
    print(above_list_price_pct)

    below_list_price_pct = round((df[df['ClosePrice'] < df['ListPrice']].shape[0] / df.shape[0]) * 100, 2)
    print(below_list_price_pct)

    at_list_price_pct = round((df[df['ClosePrice'] == df['ListPrice']].shape[0] / df.shape[0]) * 100, 2)
    print(at_list_price_pct)

    # any apparent date consistency issues?
    # convert date columns to datetime
    close_date = pd.to_datetime(df['CloseDate'], errors = 'coerce')
    list_date = pd.to_datetime(df['ListingContractDate'], errors = 'coerce')
    bought_date = pd.to_datetime(df['PurchaseContractDate'], errors = 'coerce')

    # close date before listing date
    close_before_listing = int((close_date < list_date).sum())
    print('Close date before listing date:', close_before_listing)

    # close date before bought date
    close_before_bought = int((close_date < bought_date).sum())
    print('Close date before purchase date:', close_before_bought)

    # counties w highest median close prices
    county_median_prices = df.groupby('CountyOrParish')['ClosePrice'].median()
    county_median_prices = county_median_prices.sort_values(ascending = False).reset_index(name = 'median_ClosePrice')
    print(county_median_prices.head(10))

    # save filtered dataset as new csv
    print(f'Saving {df_name} dataset to csv...')
    df.to_csv(f'./data/{df_name}.csv', index = False)

# run eda pipeline for listings dataset
eda_pipeline(listings, 'listings')

# run eda pipeline for sold dataset
eda_pipeline(sold, 'sold')