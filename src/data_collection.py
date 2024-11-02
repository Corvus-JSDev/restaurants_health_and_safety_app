import censusdis.data as ced
from censusdis.datasets import ACS5
import censusdis.states as states
import os

def download_list_of_counties():
	counties_df = ced.download(
	    dataset=ACS5,
	    vintage=2022,
	    download_variables=["NAME"],
	    state=states.ALL_STATES,
	    county="*"
	)
	counties_df[['county', 'state']] = counties_df['NAME'].str.split(', ', expand=True)
	counties_df.drop(columns=['NAME', 'STATE', 'COUNTY'], inplace=True)
	current_directory = os.path.dirname(os.path.abspath(__file__))
	counties_df.to_csv(f'{current_directory}/../data/processed/counties_with_states.csv', index=False)
