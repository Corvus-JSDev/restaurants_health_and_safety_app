import censusdis.data as ced
from censusdis.datasets import ACS5
import censusdis.states as states
import pandas as pd
import os
import sqlite3

current_directory = os.path.dirname(os.path.abspath(__file__))


def download_list_of_counties():
	counties_df = ced.download(
	    dataset=ACS5,
	    vintage=2022,
	    download_variables=["NAME"],
	    state=states.ALL_STATES,
	    county="*"
	)
	counties_df[['county', 'state']] = counties_df['NAME'].str.split(', ', expand=True)
	counties_df.drop(columns=['NAME', 'STATE', 'COUNTY'], inplace=True)  # We don't need these columns
	counties_df.to_csv(f'{current_directory}/../data/processed/counties_with_states.csv', index=False)


def create_sql_database():
	df = pd.read_csv(f'{current_directory}/../data/processed/counties_with_states.csv')
	with sqlite3.connect(f'{current_directory}/../data/sql_data/CountiesByState.db') as connect:
		for state in df['state'].unique():
			state_counties = df.loc[ df['state'] == state ][['county']]
			# Create the tables and populate them
			state_counties.to_sql(state, connect, if_exists='replace', index=False)
