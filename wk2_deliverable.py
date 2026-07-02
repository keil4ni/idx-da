# import stuff
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

# load data from wk1 folder
folder = Path('./data')

listings = pd.read_csv(folder / 'listings.csv')
sold = pd.read_csv(folder / 'sold.csv')

# SOLD DATASET
print('Sold dataset shape:', sold.shape)
print('Sold dataset columns:', sold.columns)
print('Sold data types:', sold.dtypes)
print('Sold dataset head:', sold.head())

# check property categories
print(sold['PropertyType'].unique())

# validate completeness
print('Sold dataset null values:', sold.isnull().sum())

# null-count summary table
sold_null_count = sold.isnull().sum()
sold_null_percent = sold.isnull().mean() * 100

sold_null_summary = pd.DataFrame({
    'null count': sold_null_count,
    'null percent': sold_null_percent
})

print((sold_null_summary.sort_values(by = 'null percent', ascending = False).head(10)))

# find cols w >90% nulls
sold_over90 = sold_null_summary[sold_null_summary['null percent'] > 90]
print('Sold dataset cols w >90% nulls:', sold_over90.shape[0])
# output: (15,2)

# prepare list of cols to flag if they have >90% nulls
sold_over90_cols = sold_over90.index.tolist()
print(sold_over90_cols)

# exclude core fields from flagged list if there are any
core_fields = ['ClosePrice', 'ListPrice', 'OriginalListPrice',
               'LivingArea', 'LotSizeAcres', 'BedroomsTotal',
               'BathroomsTotalInteger', 'DaysOnMarket', 'YearBuilt']

for field in core_fields:
    if field in sold_over90_cols:
        sold_over90_cols.remove(field)

# check if any flagged cols were removed
print(len(sold_over90_cols))
# output: 15

# numeric distrib review
sold_summary = sold[['ClosePrice', 'LivingArea', 'DaysOnMarket']].describe()
print(sold_summary)

# visualizations for each numeric field (histograms, boxplots, and percentile summaries, and identify extreme outliers)
for col in ['ClosePrice', 'LivingArea', 'DaysOnMarket']:
    plt.figure(figsize=(12, 4))
    
    # histogram
    plt.subplot(1, 3, 1)
    plt.hist(sold[col].dropna())
    plt.title(f'{col} Histogram')
    plt.xlabel(col)
    plt.ylabel('Frequency')
    
    # boxplot
    plt.subplot(1, 3, 2)
    plt.boxplot(sold[col].dropna())
    plt.title(f'{col} Boxplot')
    plt.ylabel(col) 
    
    # percentile summary
    plt.subplot(1, 3, 3)
    percentiles = [25, 50, 75]
    vals = sold[col].quantile([p/100 for p in percentiles])
    plt.bar([f'{p}%' for p in percentiles], vals)
    plt.title(f'{col} Percentile Summary')
    plt.ylabel(col)
    plt.savefig(f'./figs/wk2_sold_{col}_viz.png')  # save as png
    
    plt.tight_layout()
    plt.show()

# save filtered dataset as new csv
sold.to_csv('./data/sold.csv', index = False)




# LISTINGS DATASET
print('Listings dataset shape:', listings.shape)
print('Listings dataset columns:', listings.columns)
print('Listings data types:', listings.dtypes)
print('Listings dataset head:', listings.head())

# check property categories
print(listings['PropertyType'].unique())
# output: array(['Residential'], dtype=object)

# validate completeness
print('Listings dataset null values:', listings.isnull().sum())

# null-count summary table
listing_null_count = listings.isnull().sum()
listing_null_percent = listings.isnull().mean() * 100

listing_null_summary = pd.DataFrame({
    'null count': listing_null_count,
    'null percent': listing_null_percent
})

listing_null_summary.sort_values(by = 'null percent', ascending = False).head(10)

# find cols w >90% nulls
listing_over90 = listing_null_summary[listing_null_summary['null percent'] > 90]
print('Listings dataset cols w >90% nulls:', listing_over90.shape[0])

# prepare list of cols to flag if they have >90% nulls
listing_over90_cols = listing_over90.index.tolist()
print(listing_over90_cols)

# exclude core fields from flagged list if there are any
for field in core_fields:
    if field in listing_over90_cols:
        listing_over90_cols.remove(field)

# check if any flagged cols were removed
print(len(listing_over90_cols))

# numeric distrib review
listings_summary = listings[['ClosePrice', 'LivingArea', 'DaysOnMarket']].describe()
print(listings_summary)

# visualizations for each numeric field (histograms, boxplots, and percentile summaries, and identify extreme outliers)
for col in ['ClosePrice', 'LivingArea', 'DaysOnMarket']:
    plt.figure(figsize=(12, 4))
    
    # histogram
    plt.subplot(1, 3, 1)
    plt.hist(listings[col].dropna())
    plt.title(f'{col} Histogram')
    plt.xlabel(col)
    plt.ylabel('Frequency')
    
    # boxplot
    plt.subplot(1, 3, 2)
    plt.boxplot(listings[col].dropna())
    plt.title(f'{col} Boxplot')
    plt.ylabel(col)

    # percentile summary
    plt.subplot(1, 3, 3)
    percentiles = [25, 50, 75]
    vals = listings[col].quantile([p/100 for p in percentiles])
    plt.bar([f'{p}%' for p in percentiles], vals)
    plt.title(f'{col} Percentile Summary')
    plt.ylabel(col)
    plt.savefig(f'./figs/wk2_listings_{col}_viz.png')  # save as png
    
    plt.tight_layout()
    plt.show()

# save filtered dataset as new csv
listings.to_csv('./data/listings.csv', index = False)