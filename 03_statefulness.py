import streamlit as st

count = 0

increment = st.button('Increment')

if increment:
    count += 1

st.write('State of increment button: ', increment)
st.write('Count = ', count)







# if 'count' not in st.session_state:
#     st.session_state['count'] = 0

# increment = st.button('Increment')

# if increment:
#     st.session_state['count'] += 1

# st.write('State of increment button: ', increment)
# st.write('Count = ', st.session_state['count'])







# if 'count' not in st.session_state:
#     st.session_state['count'] = 0

# st.button('Increment', key='button_state')

# if st.session_state['button_state']:
#     st.session_state['count'] += 1

# st.write('State of increment button: ', st.session_state['button_state'])
# st.write('Count = ', st.session_state['count'])







# if 'count' not in st.session_state:
#     st.session_state['count'] = 0

# def increment_counter():
#     st.session_state['count'] += 1

# st.button('Increment', key='button_state', on_click=increment_counter)

# st.write('State of increment button: ', st.session_state['button_state'])
# st.write('Count = ', st.session_state['count'])

