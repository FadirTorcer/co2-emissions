import streamlit as st
import altair as alt
import requests
import pandas as pd
import os
from datetime import date, datetime
from collections import Counter
import boto3
import json

st.set_page_config(
    page_title = '311 Reported Issues',
    page_icon = ':vertical_traffic_light:',
    layout = 'centered',
    initial_sidebar_state = 'expanded'
)

# titles and headers ##############################################################################

st.title('311 Reported Issues')
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

# code and equations ##############################################################################

st.code('print(x)')

st.latex(r'\sum_{i=1}^{N} (x_i - \bar{x})^2')

st.image(
    'https://www.kcsmartsewer.us/home/showpublishedimage/4169/637305142541770000',
    width = 100
)






# # fetch data ###################################################################################

# APP_TOKEN = os.getenv('MY_APP_TOKEN')
# ENDPOINT = r"https://data.kcmo.org/resource/d4px-6rwg.json"
# DATE_FILTER = r"open_date_time>'2023-01-01'"
# STATUS_FILTER = r"current_status='resolved'"
# MAX_RECORDS = 500000

# headers={'X-App-Token': APP_TOKEN}
# query = rf"{ENDPOINT}?$select=*&$where={DATE_FILTER}&{STATUS_FILTER}&$limit={MAX_RECORDS}"

# @st.cache_data
# def get_data():

#     result = requests.get(query, headers=headers)
#     df = pd.DataFrame.from_records(result.json())

#     # convert data types
#     df['open_date_time'] = pd.to_datetime(df['open_date_time'])
#     df['latitude'] = df['latitude'].astype(float)
#     df['longitude'] = df['longitude'].astype(float)

#     # replace address with zip
#     incident_zip = df['incident_address'].fillna('').apply(lambda x: x[-5:])
#     df = df.drop('incident_address', axis=1)
#     df.insert(9, 'incident_zip', incident_zip)

#     # filter dataframe to top 10 most common issue types, so I can display stats by type
#     keep = [x0 for x0,x1 in Counter(df['issue_type']).most_common(10)][1:]
#     df = df[df['issue_type'].isin(keep)]

#     return df

# df = get_data() 

# # display data ####################################################################################

# st.write('---')
# st.subheader('311 Data')
# st.dataframe(df)











# # line chart ######################################################################################

# st.write('---')
# st.subheader('Count of Reported Issues by Week')

# # prep data

# df['open_week'] = df['open_date_time'].dt.to_period('W').apply(lambda r: r.start_time)
# df = df[~df['open_week'].isin([df['open_week'].min(), df['open_week'].max()])]

# g = df.groupby(['open_week', 'issue_type']) \
#     .agg({'reported_issue': 'count'}) \
#     .rename(columns = {'reported_issue': 'count_of_issues'}) \
#     .reset_index()
# g1 = g[['open_week', 'count_of_issues', 'issue_type']] \
#     .pivot(index='open_week', columns='issue_type', values='count_of_issues').fillna(0)

# # g1 = g.pivot(index='open_week', columns='issue_type', values='count_of_issues').fillna(0)

# # display data

# # with streamlit built-in
# st.line_chart(g1)




# # with altair
# c = alt.Chart(g).mark_line().encode(
#     color = 'issue_type',
#     x = 'open_week',
#     y = 'count_of_issues'
# ).properties(width=800)

# st.altair_chart(c)











# # map ######################################################################################

# st.write('---')
# st.subheader('Issues with City-Owned Trees by Address')

# # prep data

# data = df[df['issue_type'] == 'Trees - City Owned'].reset_index(drop=True)

# # display data

# st.map(data=data, zoom=9) 