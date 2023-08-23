# %%

# What data do I want to pull via API?
# current_status = resolved
# open_date_time > March 4, 2021 (or just pull all data, since it probably only exists in this system after this date)

import os
import pandas as pd
from sodapy import Socrata
import plotly.express as px

APP_TOKEN = os.getenv('MY_APP_TOKEN')

API_ENDPOINT = 'data.kcmo.org'
DATASET_ID = 'd4px-6rwg'
STATUS_FILTER = "current_status = 'resolved'"
DATE_FILTER = "open_date_time > '2021-03-04T00:00:00.000'"
MAX_RECORDS = 500000

client = Socrata(API_ENDPOINT, APP_TOKEN)

results = client.get(
    DATASET_ID, 
    where = f'{STATUS_FILTER} AND {DATE_FILTER}',
    limit = MAX_RECORDS)

df = pd.DataFrame.from_records(results)
df = df[df['days_to_close'].notna()]

# %% Variables to investigate
from collections import Counter

df.columns.to_list()
len(Counter(df['incident_address']))
Counter(df['department_work_group']).most_common(10)

# issue_type (52 distinct, none missing)
# issue_sub_type (300 distinct)
# department_work_group (30 distinct, none missing) - probably strongly correlated with issue_type
# incident_address (7675 missing) - maybe just use zip code?
# open_date_time is weekend
# open_date_time temperature
# open_date_time precipitation (yes/no)
# days_to_close (6341 missing)


# %%

df1 = df[['department_work_group', 'issue_type', 'issue_sub_type', 'reported_issue', 'days_to_close']]
df1 = df1.sort_values(by=['department_work_group', 'issue_type', 'issue_sub_type'])
df1 = df1.groupby(['department_work_group', 'issue_type', 'issue_sub_type']) \
    .agg({'reported_issue': 'count', 'days_to_close': 'median'}) \
    .rename(columns = {'reported_issue': 'count_of_issues', 'days_to_close': 'median_days_to_close'}) \
    .reset_index()
df1 = df1[df1['count_of_issues'] >= 300]
df1.to_csv('data.csv')

# %%
