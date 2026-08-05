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
| PropertySubType   | 447164 | 20       | SingleFamilyResidence     | 335582    |
| CountyOrParish    | 448026 | 62       | Los Angeles               | 111175    |
| MLSAreaMajor      | 387638 | 1091     | 699 - Not Defined         | 46350     |
| ListOfficeName    | 448026 | 19160    | Compass                   | 31728     |
| BuyerOfficeName   | 440892 | 21877    | Compass                   | 29629     |

> Final dataset shape: (448026, 55)

### ``LISTINGS`` SEGMENT ANALYSIS
<hr>

| variable          | count  | unique   | top                       | freq      |
| ------------------| -----: | -------: | ------------------------: | --------: |
| PropertySubType   | 605633 | 21       | SingleFamilyResidence     | 442975    |
| CountyOrParish    | 606998 | 63       | Los Angeles               | 154458    |
| MLSAreaMajor      | 524494 | 1114     | 699 - Not Defined         | 67507     |
| ListOfficeName    | 606998 | 21497    | Compass                   | 43289     |
| BuyerOfficeName   | 187658 | 14932    | Compass                   | 15036     |

> Final dataset shape: (606998, 46)

Note: School columns were dropped from both datasets