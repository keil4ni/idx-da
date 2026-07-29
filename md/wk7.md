### Week 7
Dataset shape and median values before and after filtering outliers
<hr>

#### SOLD dataset
<hr>

| Variable     | Dataset Size (Flagged) | Dataset Size (Removed) | Rows Removed | Median (Flagged) | Median (Removed) | Median Change |
| ------------ | ---------------------: | ---------------------: | -----------: | ---------------: | ---------------: | ------------: |
| ClosePrice   |                448,026 |                414,562 |       33,464 |        825,000.0 |        784,385.5 |     -40,614.5 |
| LivingArea   |                448,026 |                428,198 |       19,828 |          1,646.0 |          1,608.0 |         -38.0 |
| DaysOnMarket |                448,026 |                413,787 |       34,239 |             18.0 |             16.0 |          -2.0 |

Percentage-wise,

| Variable     | % of Rows Removed | Median Change (%) |
| ------------ | ----------------: | ----------------: |
| ClosePrice   |             7.47% |            -4.92% |
| LivingArea   |             4.43% |            -2.31% |
| DaysOnMarket |             7.64% |           -11.11% |


#### LISTINGS dataset
<hr>

| Variable     | Dataset Size (Flagged) | Dataset Size (Removed) | Rows Removed | Median (Flagged) | Median (Removed) | Median Change |
| ------------ | ---------------------: | ---------------------: | -----------: | ---------------: | ---------------: | ------------: |
| ClosePrice   |                606,998 |                162,961 |      444,037 |          860,000 |          820,000 |       -40,000 |
| LivingArea   |                606,998 |                576,563 |       30,435 |            1,672 |            1,625 |           -47 |
| DaysOnMarket |                606,998 |                549,113 |       57,885 |               11 |               10 |            -1 |

Percentage-wise,

| Variable     | % of Rows Removed | Median Change (%) |
| ------------ | ----------------: | ----------------: |
| ClosePrice   |            73.15% |            -4.65% |
| LivingArea   |             5.01% |            -2.81% |
| DaysOnMarket |             9.54% |            -9.09% |