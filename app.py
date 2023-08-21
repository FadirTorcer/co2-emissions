# %%

# What data do I want to pull via API?
# current_status = resolved
# open_date_time > March 4, 2021 (or just pull all data, since it probably only exists in this system after this date)

import os
import pandas as pd
from sodapy import Socrata

APP_TOKEN = os.getenv('MY_APP_TOKEN')

API_ENDPOINT = 'data.kcmo.org'
DATASET_ID = 'd4px-6rwg'
STATUS_FILTER = "current_status = 'resolved'"
DATE_FILTER = "open_date_time > '2021-03-04T00:00:00.000'"

client = Socrata(API_ENDPOINT, APP_TOKEN)

results = client.get(
    DATASET_ID, 
    where = f'{STATUS_FILTER} AND {DATE_FILTER}',
    limit = 500000)

results_df = pd.DataFrame.from_records(results)

results_df['open_date_time'].max()
results_df['open_date_time'].min()

# %%
