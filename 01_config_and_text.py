import streamlit as st

# %% Page Configuration ####################

st.set_page_config(
    page_title = '311 Reported Issues',
    page_icon = ':vertical_traffic_light:',
    layout = 'centered',
    initial_sidebar_state = 'expanded'
)
# other page icon options
# :speech_balloon: :house: :clipboard: :pushpin:

# %% Titles and Headers ####################

st.title('311 Reported Issues')
st.header('This is my header')

st.write('---')
st.subheader('This is my subheader')
st.write('Here is some stuff I want to write. '
         'I can use **markdown** formatting, which is pretty _cool_. '
         'And with this long string, I can see what happens '
         'when I continue text past a single line.')

st.write('---')
st.subheader('This is my second section')
st.write('It would be nice to have a divider between sections.')
st.write('''
         You can use `st.write` to make a list with markdown.
         * item 1
         * item 2
         * item 3
         * item 4
         ''')
st.write('Link to my [Github repo](https://github.com/ajander/311-reported-issues)')

# %% Code and Equations ####################

st.code('print(x)')

st.latex(r'\sum_{i=1}^{N} (x_i - \bar{x})^2')

# %% Data ####################

from sodapy import Socrata
import pandas as pd
import os

APP_TOKEN = os.getenv('MY_APP_TOKEN')
API_ENDPOINT = 'data.kcmo.org'
DATASET_ID = 'd4px-6rwg'
STATUS_FILTER = "current_status = 'resolved'"
DATE_FILTER = "open_date_time >= '2023-01-01T00:00:00.000'"  # "open_date_time > '2021-03-04T00:00:00.000'"
MAX_RECORDS = 500000  # 500000 to get all

@st.cache_data
def get_data():

    client = Socrata(API_ENDPOINT, APP_TOKEN)

    results = client.get(
        DATASET_ID, 
        where = f'{STATUS_FILTER} AND {DATE_FILTER}',
        limit = MAX_RECORDS)

    df = pd.DataFrame.from_records(results)
    df = df[df['days_to_close'].notna()]

    # replace address with zip
    incident_zip = df['incident_address'].fillna('').apply(lambda x: x[-5:])
    df = df.drop('incident_address', axis=1)
    df.insert(9, 'incident_zip', incident_zip)

    # filter dataframe to departments with the most issues, so I can display stats by dept
    from collections import Counter
    keep = [x0 for x0,x1 in Counter(df['issue_type']).most_common(10)][1:]
    df = df[df['issue_type'].isin(keep)]

    return df

df = get_data()

# %% Show dataframe ####################

st.write('---')
st.subheader('311 Data')
st.dataframe(df)

# %% Line chart ####################

import altair as alt

df['open_week'] = pd.to_datetime(df['open_date_time']).dt.to_period('W').apply(lambda r: r.start_time)

g = df.groupby(['open_week', 'issue_type']) \
    .agg({'reported_issue': 'count'}) \
    .rename(columns = {'reported_issue': 'count_of_issues'}) \
    .reset_index()

# remove first and last weeks because their counts are incomplete
g = g[~g['open_week'].isin([g['open_week'].min(), g['open_week'].max()])]

c = alt.Chart(g).mark_line().encode(
    color = 'issue_type',
    x = 'open_week',
    y = 'count_of_issues'
).properties(width=800)

st.altair_chart(c)

# %% Map ####################

data = df[df['issue_type'] == 'Property Violations'].reset_index(drop=True)
data['latitude'] = data['latitude'].astype(float)
data['longitude'] = data['longitude'].astype(float)
st.map(data=data, zoom=9)

# %%


