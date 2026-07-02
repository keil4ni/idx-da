# import stuff
import pandas as pd
import os

# store sold and listing dfs and their shapes in list
sold = []
sold_shapes = []

listing = []
listing_shapes = []

END_MONTH = 5

# get files from each month from years 2024-2026
for year in [2024, 2025, 2026]:
    for month in range(1, 13):
        # stop loop after fully completed calendar month
        if year == 2026 and month > END_MONTH:
            break

        # GET SOLD CSV'S
        # note: there are normal file csv's and filled file csv's
        base_sold = f'./data/CRMLSSold{year}{month:02d}.csv'
        filled_sold = f'./data/CRMLSSold{year}{month:02d}_filled.csv'

        # append filled csv if it exists, otherwise append the regular file
        if os.path.exists(filled_sold):
            sold_df = pd.read_csv(filled_sold)
            sold_df = sold_df.iloc[:, :-2] # drop last 2 cols of filled file
        elif os.path.exists(base_sold):
            sold_df = pd.read_csv(base_sold)
        else:
            continue

        # GET LISTING CSV'S
        # note: listing csv files follow the same name scheme unlike sold csv files
        base_listing = f'./data/CRMLSListing{year}{month:02d}.csv'
        # append csv if it exists, otherwise continue
        if os.path.exists(base_listing):
            listing_df = pd.read_csv(base_listing)
        else:
            continue
            
        listing.append(listing_df)
        listing_shapes.append(listing_df.shape[0])
            
        sold.append(sold_df)
        sold_shapes.append(sold_df.shape[0])



# CHECK SOLD CSV ROW COUNTS, FILTER, THEN SAVE
print('Total sold row count before concat:', sum(sold_shapes))
sold_df = pd.concat(sold)
print('Total sold row count after concat (and before filtering):', sold_df.shape)
# sold_df.head()
# ROW COUNT: 640526

# filter property type by residential
filtered_sold = sold_df[sold_df['PropertyType'] == 'Residential']

print('Total sold row count after filtering:', filtered_sold.shape)
# filtered_sold.head()
# ROW COUNT: 430716



# CHECK LISTING CSV ROW COUNTS, FILTER, THEN SAVE
print('Total listing row count before concat:', sum(listing_shapes))
listing_df = pd.concat(listing)
print('Total listing row count after concat (and before filtering):', listing_df.shape)
# listing_df.head()
# ROW COUNT: 917740

# filter property type by residential
filtered_listing = listing_df[listing_df['PropertyType'] == 'Residential']

print('Total listing row count after filtering:', filtered_listing.shape)
# filtered_listing.head()
# ROW COUNT: 583650



# SAVE filtered dataframes as csv file
filtered_sold.to_csv('./data/sold.csv', index = False)
filtered_listing.to_csv('./data/listings.csv', index = False)

