# IDX Exchange Data Analyst Internship

### Week 0 deliverables
- ``crmls_listed.py`` extracts information from listed csv files via API calls
- ``crmls_sold.py`` extracts information from sold csv files via API calls

### Week 1 deliverables
- ``wk1_deliverable.py`` concatenates all monthly datasets starting from January 2024 up to the most recently completed calendar month & filters by the residential property type

### Week 2-3 deliverables
- ``wk2_deliverable.py`` documents unique property types found, creates a null-count summary table, missing value report that flags columns with >90% nulls, and numeric distribution summary + visualizations for variables ``ClosePrice``, ``LivingArea``, ``DaysOnMarket``
- ``wk2_deliverable.ipynb`` breaks down the above py script into code blocks & also answers the EDA questions (WIP)
- ``wk3_deliverable.py`` fetches live data from FRED API, resamples to monthly averages, merges them into sold & listings datasets using year_month key, & performs validation check to confirm there are no nulls

### Week 4-5 deliverables
- WIP
- WIP