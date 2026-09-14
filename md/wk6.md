## Week 6
Summary statistics of the following fields (if available):
- ``PropertySubType``
- ``CountyOrParish``
- ``MLSAreaMajor``
- ``ListOfficeName``
- ``BuyerOfficeName``
<hr>

### ``SOLD`` SEGMENT ANALYSIS
<hr>

| variable          | count  | unique   | top                       | freq      |
| ------------------| -----: | -------: | ------------------------: | --------: |
| PropertySubType   | 479223 | 20       | SingleFamilyResidence     | 359760    |
| CountyOrParish    | 480134 | 60       | Los Angeles               | 119245    |
| MLSAreaMajor      | 415078 | 1092     | 699 - Not Defined         | 48980     |
| ListOfficeName    | 480134 | 19624    | Compass                   | 34009     |
| BuyerOfficeName   | 472634 | 22452    | Compass                   | 31800     |

> Final dataset shape: (480134, 55)

### ``LISTINGS`` SEGMENT ANALYSIS
<hr>

| variable          | count  | unique   | top                       | freq      |
| ------------------| -----: | -------: | ------------------------: | --------: |
| PropertySubType   | 651860 | 21       | SingleFamilyResidence     | 476252    |
| CountyOrParish    | 653323 | 63       | Los Angeles               | 166687    |
| MLSAreaMajor      | 564385 | 1116     | 699 - Not Defined         | 72814     |
| ListOfficeName    | 653323 | 22009    | Compass                   | 46576     |
| BuyerOfficeName   | 191414 | 15045    | Compass                   | 15470     |

> Final dataset shape: (653323, 46)

Note: School columns were dropped from both datasets