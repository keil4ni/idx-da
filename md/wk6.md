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
| PropertySubType   | 464155 | 20       | SingleFamilyResidence     | 348347    |
| CountyOrParish    | 465039 | 60       | Los Angeles               | 115475    |
| MLSAreaMajor      | 402189 | 1091     | 699 - Not Defined         | 47718     |
| ListOfficeName    | 465039 | 19410    | Compass                   | 32942     |
| BuyerOfficeName   | 457713 | 22189    | Compass                   | 30834     |

> Final dataset shape: (465039, 55)

### ``LISTINGS`` SEGMENT ANALYSIS
<hr>

| variable          | count  | unique   | top                       | freq      |
| ------------------| -----: | -------: | ------------------------: | --------: |
| PropertySubType   | 629830 | 21       | SingleFamilyResidence     | 460366    |
| CountyOrParish    | 631250 | 63       | Los Angeles               | 160877    |
| MLSAreaMajor      | 545384 | 1116     | 699 - Not Defined         | 70282     |
| ListOfficeName    | 631250 | 21763    | Compass                   | 45015     |
| BuyerOfficeName   | 189227 | 14985    | Compass                   | 15216     |

> Final dataset shape: (631250, 46)

Note: School columns were dropped from both datasets