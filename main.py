import streamlit as st  # python3 -m streamlit run main.py
from src import helpers
import os
import pandas as pd
from sodapy import Socrata
from dotenv import load_dotenv
load_dotenv()

MY_KEY = os.getenv('MY_KEY')

amongus = chr(sum(range(ord(min(str(not()))))))  # The among us character, lol

with st.spinner('Loading...'):
	print("\n  ----- Checking Prerequisites -----\n")
	helpers.ensure_county_data_is_installed()
	helpers.ensure_sql_database_exists()
	print("\n  ----- Prerequisites Complete -----\n")


# === HERO ===
st.title("App Name")
st.write("Find how discussing the restaurants you go to really are (still a work in progress...)")


# === LOCATION SELECTION ===
list_of_states = helpers.get_list_of_states()
st.markdown('##### Select State')
selected_state = st.selectbox(label='Select State', options=list_of_states, index=helpers.loc_state(list_of_states),
	placeholder='Find your state', label_visibility='collapsed')

st.markdown('##### Select County')
list_of_counties = helpers.get_list_of_counties(selected_state)
selected_county = st.selectbox(label='Select County', options=list_of_counties, index=None,
	placeholder='Find your county', label_visibility='collapsed')
