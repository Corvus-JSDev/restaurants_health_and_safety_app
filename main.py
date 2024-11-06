import streamlit as st  # python3 -m streamlit run main.py
from src import helpers
from src import data_collection
import os
import pandas as pd
from sodapy import Socrata
from dotenv import load_dotenv
load_dotenv()

# === PREREQUISITES ===
st.set_page_config(
	page_title='Resturant Health Inspection Records',
	page_icon=":shark:",
	menu_items={
		'Get Help': 'https://www.linktogithubrepo.com',
		'Report a bug': "https://www.linktogithubrepo/issues.com",
		'About': "https://www.linktoanotherpagethatdescribeshowtouseit.com"
	}
)
st.warning('For the latest information, check your local health department\'s website.')

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
selected_state = st.selectbox(label='Select State', options=list_of_states,
	index=helpers.loc_state(list_of_states),
	placeholder='Find your state', label_visibility='collapsed')
selected_state = selected_state.lower() if selected_state else None


st.markdown('##### Select County')
list_of_counties = helpers.get_list_of_counties(selected_state)
selected_county = st.selectbox(label='Select County', options=list_of_counties,
	index=None, placeholder='Find your county', label_visibility='collapsed')



# === GETTING INSPECTION DATA ===
df = None
match selected_state:
	case 'new york':
		with st.spinner('Loading...'):
			df = data_collection.get_NY_health_inspection_data(selected_county)
	case _:
		df = 'state not supported'

if df == 'state not supported':
	st.markdown("""
		##### Uh-oh, we currently do not have access to your state's inspection data.

		This could be due to a few reasons. Most commonly, your state may not provide public access to its inspection data via APIs. Another possibility is that since this app is still in its early stages, the developers have not yet researched, processed, or implemented data for every state.

		Try searching for:      *[Your County/City]* Health Department restaurant inspections
		""")
elif not df.empty:
		st.dataframe(df, hide_index=True)
else:
	st.markdown("""
		##### Sorry, we don't have data for this county yet.

		This app is still being worked on, and not all states share their health data or allow us to get live updates.

		Try searching for:      *[Your County/City]* Health Department restaurant inspections
		""")
