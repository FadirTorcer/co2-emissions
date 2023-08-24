import streamlit as st

st.set_page_config(
    page_title = '311 Reported Issues',
    page_icon = ':vertical_traffic_light:',
    layout = 'wide',
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