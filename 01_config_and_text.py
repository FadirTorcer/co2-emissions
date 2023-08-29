import streamlit as st

st.set_page_config(
    page_title = 'Watching Emissions',
    page_icon = ':earth_americas:',
    layout = 'centered',
    initial_sidebar_state = 'expanded'
)











# # titles and headers ##############################################################################

st.title('Watching Emissions')
st.header('Natural Gas Emissions Per State')
st.write('Total Carbon Dioxide Emissions From All Sectors')

st.write('---')
st.subheader('Data Source')
st.write('**Source:** U.S. Energy Information Administration \n')
st.write('**Release:** Energy-Related CO2 Emissions by State \n'
        '**Units:**  Million Metric Tons CO2, Not Seasonally Adjusted '
        '**Frequency:**  Annual '
        'See the EIA\'s report on Energy-Related Carbon Dioxide Emissions by State for technical notes and documentation. '
        '**Suggested Citation:** '
        'U.S. Energy Information Administration, Total Carbon Dioxide Emissions From All Sectors, Natural Gas for United States '
        '[EMISSCO2TOTVTTNGUSA], retrieved from FRED, Federal Reserve Bank of St. Louis; https://fred.stlouisfed.org/series/EMISSCO2TOTVTTNGUSA, August 28, 2023.')

# st.write('---')
# st.subheader('This is my second section')
# st.write('It would be nice to have a divider between sections.')
# st.write('''
#          You can use `st.write` to make a list with markdown.
#          * item 1
#          * item 2
#          * item 3
#          * item 4
#          ''')
# st.write('Link to my [Github repo](https://github.com/FadirTorcer/co2-emissions)')









# # code and equations ##############################################################################

# st.code('print(x)')

# st.latex(r'\sum_{i=1}^{N} (x_i - \bar{x})^2')

# st.image(
#     'https://www.kcsmartsewer.us/home/showpublishedimage/4169/637305142541770000',
#     width = 100
# )