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
    layout = 'wide',
    initial_sidebar_state = 'expanded'
)

# fetch data ###################################################################################

APP_TOKEN = os.getenv('MY_APP_TOKEN')
ENDPOINT = r"https://data.kcmo.org/resource/d4px-6rwg.json"
DATE_FILTER = r"open_date_time>'2023-01-01'"
STATUS_FILTER = r"current_status='resolved'"
MAX_RECORDS = 500000

headers={'X-App-Token': APP_TOKEN}
query = rf"{ENDPOINT}?$select=*&$where={DATE_FILTER}&{STATUS_FILTER}&$limit={MAX_RECORDS}"

@st.cache_data
def get_data():

    result = requests.get(query, headers=headers)
    df = pd.DataFrame.from_records(result.json())

    # convert data types
    df['open_date_time'] = pd.to_datetime(df['open_date_time'])
    df['latitude'] = df['latitude'].astype(float)
    df['longitude'] = df['longitude'].astype(float)

    # replace address with zip
    incident_zip = df['incident_address'].fillna('').apply(lambda x: x[-5:])
    df = df.drop('incident_address', axis=1)
    df.insert(9, 'incident_zip', incident_zip)

    # filter dataframe to top 10 most common issue types, so I can display stats by type
    keep = [x0 for x0,x1 in Counter(df['issue_type']).most_common(10)][1:]
    df = df[df['issue_type'].isin(keep)]

    return df

df = get_data()

# put data ###################################################################################

BUCKET = 'reported-issues'

s3 = boto3.resource(
    service_name = 's3',
    region_name = os.getenv('AWS_DEFAULT_REGION'),
    aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
)

s3_bucket = s3.Bucket(name=BUCKET)

def put_data(data_string, current_datetime):
    s3_bucket.put_object(
        Key = f'submitted_311_issues/{current_datetime}.json',
        Body = data_string
    )

# sidebar ######################################################################################

all_zips = [x for x in sorted(df['incident_zip'].unique()) if len(x) > 1]

def update_zips():
    st.session_state['zips'] = [st.session_state['zip_selector']]

with st.sidebar:

    st.image(
        'https://www.kcsmartsewer.us/home/showpublishedimage/4169/637305142541770000',
        width = 100
    )
    
    st.write('Show data by zipcode')

    st.checkbox(
        label = 'Show all zipcodes',
        value = True,
        key = 'zip_checkbox'
    )
    
    if st.session_state['zip_checkbox']:
        st.session_state['zips'] = all_zips
    else:
        st.selectbox(
            label = 'Select a zipcode',
            options = all_zips,
            index = 0,
            key = 'zip_selector',
            on_change = update_zips
        )
        if 'zip_selector' not in st.session_state:
            st.session_state['zips'] = all_zips
        
df = df[df['incident_zip'].isin(st.session_state['zips'])]      

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

# display data ####################################################################################

st.write('---')
st.subheader('311 Data')
st.dataframe(df)

# line chart ######################################################################################

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
g = g.pivot(index='open_week', columns='issue_type', values='count_of_issues').fillna(0)

col1, col2 = st.columns(2)

# filter data

with col2:

    if 'issue_selector' not in st.session_state:
        st.session_state['issue_selector'] = g.columns.to_list()

    selected_types = st.multiselect(
        label = 'Select one or more issue types',
        options = g.columns.to_list(),
        key = 'issue_selector'
    )

# display data

with col1:

    # with streamlit built-in
    st.line_chart(g[st.session_state['issue_selector']])

    # # with altair
    # c = alt.Chart(g[g['issue_type'].isin(st.session_state['issue_selector'])]).mark_line().encode(
    #     color = 'issue_type',
    #     x = 'open_week',
    #     y = 'count_of_issues'
    # ).properties(width=800)

    # st.altair_chart(c)

col1, col2 = st.columns(2)

with col1:

    # map ######################################################################################

    st.write('---')
    st.subheader('Issues with City-Owned Trees by Address')

    # prep data

    data = df[df['issue_type'] == 'Trees - City Owned'].reset_index(drop=True)

    # filter data

    default_start_date = date(2023, 1, 1)
    default_end_date = date(2023, 7, 31)

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

with col2:

    st.write('---')
    st.subheader('Report a New Issue')
    
    with st.form('issue_form'):
   
        st.write('Complete this form to report a new issue')

        form_issue_type = st.selectbox(
            label = 'Issue Type',
            options = df['issue_type'].unique(),
            key = 'form_issue_type'
        )

        form_issue_sub_type = st.selectbox(
            label = 'Issue Subtype',
            options = df['issue_sub_type'].unique(),
            key = 'form_issue_sub_type'
        )

        form_zipcode = st.text_input(
            label = 'Incident Zipcode',
            value = '',
            max_chars = 5,
            key = 'form_zipcode'
        )

        submitted = st.form_submit_button('Submit')

        if submitted:
            current_datetime = datetime.now().strftime('%Y%m%d_%H%M%S')
            data_dict = {
                'open_date_time': current_datetime,
                'issue_type': form_issue_type,
                'issue_sub_type': form_issue_sub_type,
                'issue_zipcode': form_zipcode
            }
            data_string = json.dumps(data_dict, indent=2, default=str) 
            put_data(data_string, current_datetime)
            st.write('Thank you for submitting your issue!')

