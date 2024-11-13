from censusdis.impl.geometry import T
import streamlit as st  # python3 -m streamlit run main.py
from src import helpers, styling
from src import data_collection
import os
import pandas as pd
from sodapy import Socrata
from dotenv import load_dotenv
load_dotenv()

# === PREREQUISITES ===
st.set_page_config(
	page_title='Resturant Health Inspection Records',
	page_icon=":shark:",  # TODO: Get a real favicon
	menu_items={
		'Get Help': 'https://www.linktogithubrepo.com',
		'Report a bug': "https://www.linktogithubrepo/issues.com",
		'About': "https://www.linktoanotherpagethatdescribeshowtouseit.com"
	}
)

with st.spinner('Loading Page...'):
	print("\n  ----- Checking Prerequisites -----\n")
	helpers.ensure_county_data_is_installed()
	helpers.ensure_sql_database_exists()
	print("\n  ----- Prerequisites Complete -----\n")

@st.dialog("Disclaimer")
def disclaimer():
    st.markdown(f"""
    For the most up-to-date information, we recommend searching for:      [Your County/City] Health Department restaurant inspections.

    This app pulls data from multiple sources, with the majority coming from government databases. However, some states do not provide public access to their databases via APIs, while others only allow API access through third-party services. This creates challenges for development, as we are left with two main options: use the available API, which may provide incomplete or outdated data, or download the database in bulk, which can quickly become outdated (often within a month or two).

    As a result, obtaining up-to-date data can be difficult. This app is designed to give you a rough idea of the cleanliness of nearby restaurants, but it may not always reflect the most current information. Also, keep in mind that some agencies only require health inspections 1-3 times per year.
    """)
col1, col2 = st.columns([5, 1])
with col1:
		st.info('For the latest information, check your local health department\'s website.')
with col2:
		if st.button("Learn More"):
			disclaimer()



# === HERO ===
st.markdown(f"""
## Restaurant Health Inspection Reports

Just enter your state and county (or city) to see a list of local restaurants and their health inspection records. It’s an easy way to check how your favorite spots stack up when it comes to cleanliness and safety!

Supported States: {", ".join(helpers.list_of_supported_states).title()}
""")
st.write(" ")


# === LOCATION SELECTION ===
st.markdown('#### Select State')
selected_state = st.selectbox(label='Select State',
	options=helpers.get_list_of_states(),
	index=helpers.loc_state(),
	placeholder='Find your state', label_visibility='collapsed')
selected_state = selected_state.lower() if selected_state else None


st.markdown('#### Select County/City')
selected_county = st.selectbox(label='Select County',
	options=helpers.get_list_of_counties(selected_state) if selected_state else ['Please select your state'],
	index=None,
	placeholder='Find your county', label_visibility='collapsed')



# === GETTING INSPECTION DATA ===
data = None

# Finding data based on user selections
if selected_state and selected_county:
	with st.spinner(f'Loading {selected_state.title()}...'):
		match selected_state:
			case 'new york':
				data = data_collection.get_NY_health_inspection_data(selected_county)
			case 'pennsylvania':
				st.warning("Note: The database we have access to for PA is out of date.")
				data = data_collection.get_PA_health_inspection_data(selected_county)
			case 'delaware':
				data = data_collection.get_DE_health_inspection_data(selected_county)

			case _:
				data = 'state not supported'
elif selected_state:
	data = "state not supported" if selected_state not in helpers.list_of_supported_states else None


# Displaying data and coloring its rows
if data == None:
	# This if statement is needed because, for reasons I can not figure out, a rare error will pop up where it says "AttributeError: module 'pandas.io.formats' has no attribute 'style'" so this is here to hide that.
	st.write(" ")
elif type(data) == str and selected_state:
	st.markdown(f"""
		#### Uh-oh, we currently do not have access to {selected_state.title()}\'s inspection data.

		This could be due to a few reasons. Most commonly, your state may not provide public access to its inspection data via APIs. Another possibility is that since this app is still in its early stages, the developers have not yet researched, processed, or implemented data for every state.

		Try searching for:   *[Your County/City]* Health Department restaurant inspections
		""")
elif isinstance(data, pd.io.formats.style.Styler) and data.data.empty:
	st.markdown(f"""
		#### Sorry, we don't have data for {selected_county} yet.

		This app is still being worked on, and not all states share their health data or allow us to get live updates for all of their counties.

		Try searching for:   *[Your County/City]* Health Department restaurant inspections
		""")
elif isinstance(data, pd.io.formats.style.Styler):
	data = data.apply(styling.highlight_alternate_rows)
	st.dataframe(data, hide_index=True)
