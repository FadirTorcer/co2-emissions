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
    page_title = 'Watching Emissions',
    page_icon = ':earth_americas:',
    layout = 'centered',
    initial_sidebar_state = 'expanded'
)

# titles and headers ##############################################################################

st.title('Watching Emissions')
st.header('Natural Gas Emissions Per State')
st.write('Total Carbon Dioxide Emissions From All Sectors')

st.write('---')
st.subheader('Data Source')
st.write('**Source:**  U.S. Energy Information Administration')
st.write('**Release:**  Energy-Related CO2 Emissions by State')
st.write('**Units:**  Million Metric Tons CO2, Not Seasonally Adjusted')
st.write('**Frequency:**  Annual')
st.write('See the EIA\'s report on Energy-Related Carbon Dioxide Emissions by State for technical notes and documentation.')
st.write('**Suggested Citation:** '
        'U.S. Energy Information Administration, Total Carbon Dioxide Emissions From All Sectors, Natural Gas for United States '
        '[EMISSCO2TOTVTTNGUSA], retrieved from FRED, Federal Reserve Bank of St. Louis; https://fred.stlouisfed.org/series/EMISSCO2TOTVTTNGUSA, August 28, 2023.')
st.image(
    'https://fred.stlouisfed.org/images/fred-logo-2x.png',
    width = 200
)

st.write('---')
st.subheader('What can we learn from this data?')
st.write('How do these total emissions relate to population?')
st.write('''
         * Does population have an obvious correlation to total carbon emissions?
         * What other factors can be linked changes in total carbon emissions? Power sources? Industry?
         * Null hypothesis: Population size/growth has no correlation to total carbon emissions.
         * Is it something not either/or? Do some states have correlation and others do not? Can we learn how to address emissions from those cases?
         ''')
st.write('Link to the [Github repo](https://github.com/FadirTorcer/co2-emissions) for this page.')

# code and equations ##############################################################################

# st.code('print(x)')

# st.latex(r'\sum_{i=1}^{N} (x_i - \bar{x})^2')

# st.image(
#     'https://www.kcsmartsewer.us/home/showpublishedimage/4169/637305142541770000',
#     width = 100
# )






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