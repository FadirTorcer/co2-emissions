import streamlit as st
import altair as alt
from sodapy import Socrata
import pandas as pd
import os
from datetime import date
from collections import Counter

# Page Configuration ####################

st.set_page_config(
    page_title = '311 Reported Issues',
    page_icon = ':vertical_traffic_light:',
    layout = 'centered',
    initial_sidebar_state = 'expanded'
)

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
    # df = df[df['days_to_close'].notna()]

    # convert data types
    df['open_date_time'] = pd.to_datetime(df['open_date_time'])
    df['latitude'] = df['latitude'].astype(float)
    df['longitude'] = df['longitude'].astype(float)

    # replace address with zip
    incident_zip = df['incident_address'].fillna('').apply(lambda x: x[-5:])
    df = df.drop('incident_address', axis=1)
    df.insert(9, 'incident_zip', incident_zip)

    # filter dataframe to departments with the most issues, so I can display stats by dept
    keep = [x0 for x0,x1 in Counter(df['issue_type']).most_common(10)][1:]
    df = df[df['issue_type'].isin(keep)]

    return df

df = get_data()

# Titles and Headers ####################

st.title('311 Reported Issues, 2023')
st.header('This is my header')
st.write('Only includes top 10 most common issue types')

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

# Code and Equations ####################

st.code('print(x)')

st.latex(r'\sum_{i=1}^{N} (x_i - \bar{x})^2')

# Show dataframe ####################

st.write('---')
st.subheader('311 Data')
st.dataframe(df)

# Line chart ####################

st.write('---')
st.subheader('Count of Reported Issues by Week')

# prep data

df['open_week'] = df['open_date_time'].dt.to_period('W').apply(lambda r: r.start_time)
df = df[~df['open_week'].isin([df['open_week'].min(), df['open_week'].max()])]

g = df.groupby(['open_week', 'issue_type']) \
    .agg({'reported_issue': 'count'}) \
    .rename(columns = {'reported_issue': 'count_of_issues'}) \
    .reset_index()

g = g[['open_week', 'count_of_issues', 'issue_type']]
g1= g.pivot(index='open_week', columns='issue_type', values='count_of_issues').fillna(0)

# filter data

if 'issue_selector' not in st.session_state:
    st.session_state['issue_selector'] = g1.columns.to_list()

selected_types = st.multiselect(
    label = 'Select one or more issue types',
    options = g1.columns.to_list(),
    key = 'issue_selector'
)

# display data

st.line_chart(g1[st.session_state['issue_selector']])

# c = alt.Chart(g[g['issue_type'].isin(st.session_state['issue_selector'])]).mark_line().encode(
#     color = 'issue_type',
#     x = 'open_week',
#     y = 'count_of_issues'
# ).properties(width=800)

# st.altair_chart(c)

# Map ####################

st.write('---')
st.subheader('"Trees - City Owned" Issues by Address')

# prep data

data = df[df['issue_type'] == 'Trees - City Owned'].reset_index(drop=True)

# filter data

default_start_date = data['open_date_time'].dt.date.min()
default_end_date = data['open_date_time'].dt.date.max()

if 'date_picker' not in st.session_state:
    st.session_state['start_date'] = default_start_date
    st.session_state['end_date'] = default_end_date
elif len(st.session_state['date_picker']) == 1:
    st.session_state['start_date'] = st.session_state['date_picker'][0]
    st.session_state['end_date'] = default_end_date
elif len(st.session_state['date_picker']) == 2:
    st.session_state['start_date'] = st.session_state['date_picker'][0]
    st.session_state['end_date'] = st.session_state['date_picker'][1]

st.date_input(
    label = 'Date Range',
    value = [default_start_date, default_end_date],
    min_value = default_start_date,
    max_value = default_end_date,
    key = 'date_picker'
)

# display data

filtered_data = data[(data['open_date_time'].dt.date >= st.session_state['start_date']) & \
                     (data['open_date_time'].dt.date <= st.session_state['end_date'])]

st.map(data=filtered_data, zoom=9)


