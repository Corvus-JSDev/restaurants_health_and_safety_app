import streamlit as st  # python3 -m streamlit run main.py
from src import helpers

# Print the among us character
amongus = chr(sum(range(ord(min(str(not()))))))

# print(f"\n----- Prerequisite Checks -----\n")
# helpers.ensure_county_data_is_installed()
# helpers.ensure_sql_database_exists()
# print(f"\n----- Prerequisite Complete! -----\n")

st.title("App Name")
st.write("Find how discussing the restaurants you go to really are (still a work in progress...)")

# NOTE: Get the users loc and add that to the index arg
list_of_states = helpers.get_list_of_states()
selected_state = st.selectbox(label='Select State', options=list_of_states)

# NOTE: Get the users loc and add that to the value arg
list_of_counties = helpers.get_list_of_counties(selected_state)
selected_county = st.selectbox(label='Search for county', options=list_of_counties)
