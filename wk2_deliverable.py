# import stuff
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

# load data from wk1 folder
folder = Path('../wk1')

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

# numeric distrib summary
sold_summary = sold[['ClosePrice', 'LivingArea', 'DaysOnMarket']].describe()
print(sold_summary)

