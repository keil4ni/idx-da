## Week 7
Dataset shape and median values before and after filtering outliers
<hr>

### SOLD dataset
<hr>

| Variable     | Dataset Size (Flagged) | Dataset Size (Removed) | Rows Removed | Median (Flagged) | Median (Removed) | Median Change |
| ------------ | ---------------------: | ---------------------: | -----------: | ---------------: | ---------------: | ------------: |
| ClosePrice   |                465,039 |                450,057 |       14,982 |        825,000.0 |        805,000.0 |     -20,000.0 |
| LivingArea   |                465,039 |                459,659 |        5,380 |          1,646.0 |          1,636.0 |         -10.0 |
| DaysOnMarket |                465,039 |                452,604 |       12,435 |             18.0 |             18.0 |           0.0 |

Percentage-wise,

| Variable     | % of Rows Removed | Median Change (%) |
| ------------ | ----------------: | ----------------: |
| ClosePrice   |             3.22% |            -2.42% |
| LivingArea   |             1.16% |            -0.61% |
| DaysOnMarket |             2.67% |             0.00% |


### LISTINGS dataset
<hr>

| Variable     | Dataset Size (Flagged) | Dataset Size (Removed) | Rows Removed | Median (Flagged) | Median (Removed) | Median Change |
| ------------ | ---------------------: | ---------------------: | -----------: | ---------------: | ---------------: | ------------: |
| ClosePrice   |                631,250 |                171,374 |      459,876 |        860,000.0 |        845,000.0 |     -15,000.0 |
| LivingArea   |                631,250 |                620,859 |       10,391 |          1,672.0 |          1,656.0 |         -16.0 |
| DaysOnMarket |                631,250 |                604,626 |       26,624 |             11.0 |             11.0 |           0.0 |

Percentage-wise,

| Variable     | % of Rows Removed | Median Change (%) |
| ------------ | ----------------: | ----------------: |
| ClosePrice   |            72.85% |            -1.74% |
| LivingArea   |             1.65% |            -0.96% |
| DaysOnMarket |             4.22% |             0.00% |