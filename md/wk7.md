## Week 7
Dataset shape and median values before and after filtering outliers
<hr>

### SOLD dataset
<hr>

| Variable                     | Dataset Size (Flagged) | Dataset Size (Removed) | Rows Removed | Median (Flagged) | Median (Removed) | Median Change |
| ---------------------------- | ---------------------: | ---------------------: | -----------: | ---------------: | ---------------: | ------------: |
| ClosePrice                   |                480,134 |                464,672 |       15,462 |        825,000.0 |        805,000.0 |     -20,000.0 |
| LivingArea                   |                480,134 |                474,590 |        5,544 |          1,647.0 |          1,637.0 |         -10.0 |
| DaysOnMarket                 |                480,134 |                467,285 |       12,849 |             19.0 |             18.0 |          -1.0 |
| close_to_original_list_ratio |                480,134 |                465,483 |       14,651 |         0.994949 |         0.994286 |     -0.000663 |

Percentage-wise,

| Variable                     | % of Rows Removed | Median Change (%) |
| ---------------------------- | ----------------: | ----------------: |
| ClosePrice                   |             3.22% |            -2.42% |
| LivingArea                   |             1.15% |            -0.61% |
| DaysOnMarket                 |             2.68% |            -5.26% |
| close_to_original_list_ratio |             3.05% |            -0.07% |

**### LISTINGS dataset**
<hr>

| Variable                     | Dataset Size (Flagged) | Dataset Size (Removed) | Rows Removed | Median (Flagged) | Median (Removed) | Median Change |
| ---------------------------- | ---------------------: | ---------------------: | -----------: | ---------------: | ---------------: | ------------: |
| ClosePrice                   |                653,323 |                172,827 |      480,496 |        860,000.0 |        846,000.0 |     -14,000.0 |
| LivingArea                   |                653,323 |                642,545 |       10,778 |          1,671.0 |          1,656.0 |         -15.0 |
| DaysOnMarket                 |                653,323 |                623,752 |       29,571 |             11.0 |             11.0 |           0.0 |
| close_to_original_list_ratio |                653,323 |                171,148 |      482,175 |              1.0 |              1.0 |           0.0 |

Percentage-wise,

| Variable                     | % of Rows Removed | Median Change (%) |
| ---------------------------- | ----------------: | ----------------: |
| ClosePrice                   |            73.55% |            -1.63% |
| LivingArea                   |             1.65% |            -0.90% |
| DaysOnMarket                 |             4.53% |             0.00% |
| close_to_original_list_ratio |            73.80% |             0.00% |