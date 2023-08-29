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









# # code and equations ##############################################################################

# st.code('print(x)')

# st.latex(r'\sum_{i=1}^{N} (x_i - \bar{x})^2')