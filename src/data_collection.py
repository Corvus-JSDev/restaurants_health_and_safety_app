#from re import L
import censusdis.data as ced
from censusdis.datasets import ACS5
import censusdis.states as states
import pandas as pd
import os
import sqlite3
from sodapy import Socrata
from datetime import date
from dateutil.relativedelta import relativedelta
from dotenv import load_dotenv
load_dotenv()

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


NY_APP_TOKEN = os.getenv('NY_APP_TOKEN') or None
def get_NY_health_inspection_data(county, resturant_name=''):
	county = county.split()[0].upper()  # The reason we use upper is because gov APIs suck.
	resturant_query = f'AND facility == \'{resturant_name}\'' if resturant_name else ''
	county_query = f'AND county == \'{county}\'' if county else ''

	# The query that will be pulling only the needed data (pulling data from 5 years ago from today)
	query = f"""
	SELECT
	    *
	WHERE
	    date > '{str(date.today() - relativedelta(years=5))}'
		{county_query}
	"""

	# Getting the data itself
	client = Socrata("health.data.ny.gov", NY_APP_TOKEN)
	results = client.get("cnih-y5dw", query=query)
	client.close()

	df = pd.DataFrame.from_records(results)

	# This is here because for some reason NY doesn't want to share their data for some counties. Can you tell I hate working with gov APIs yet? Like honestly, how hard is it to have data for all of YOUR OWN counties?
	if df.empty:
		return df


	# Add a count of one to all the rows so when we group them we can count how many inspections that place has had over the given time
	df['Number Of Inspections'] = 1
	# Converting objs to ints
	df['total_critical_violations'] = df['total_critical_violations'].astype(int)
	df['total_crit_not_corrected'] = df['total_crit_not_corrected'].astype(int)
	df['total_noncritical_violations'] = df['total_noncritical_violations'].astype(int)

	# Grouping and renameing
	df = df.groupby('address').agg({
	    "facility": 'last',
	    "total_critical_violations": "sum",
	    "total_crit_not_corrected": "sum",
	    "total_noncritical_violations": "sum",
	    "Number Of Inspections": "sum",
	    'date': 'min'
	}).reset_index().rename(columns={
	    "facility": 'Name',
	    "total_critical_violations": "Critical Violations",
	    "total_crit_not_corrected": "Repeat Violations",
	    "total_noncritical_violations": "Minor Violations",
	    'date': 'Earliest Recorded Inspection',
		'address': 'Address'
	})


	def calc_risk_score(row):
		inspection_count = row['Number Of Inspections']
		if inspection_count < 3:
			return "N/A"
		else:
			answer = (((row['Repeat Violations'] + (0.50 * row['Repeat Violations'])) + row['Critical Violations'] + (row['Minor Violations'] - (0.30 * row['Minor Violations']))) / inspection_count)
			return str(round(answer, 1))

	# Finishing touches
	df['Risk Score'] = df.apply(calc_risk_score, axis=1)
	df['Name'] = df['Name'].str.title()
	df['Address'] = df['Address'].str.title()
	df['Earliest Recorded Inspection'] = df['Earliest Recorded Inspection'].str.split('T').str.get(0)

	df = df.rename(columns={'Earliest Recorded Inspection': "Earliest Recorded Inspection (Y-M-D)"})
	# Moves the risk score and name column to the front
	cols = ['Risk Score', 'Name'] + [col for col in df.columns if col != 'Risk Score' and col != 'Name']


	return df[cols]


PA_APP_TOKEN = os.getenv('PA_APP_TOKEN') or None
def get_PA_health_inspection_data(county, resturant_name=''):
    county = county.split()[0].title()
    county_query = f'county_name == \'{county}\'' if county else ''
    resturant_query = f'AND facility == \'{resturant_name}\'' if resturant_name else ''

    # The query that will be pulling only the needed data (pulling data from 5 years ago from today)
    query = f"""
    SELECT
        *
    WHERE
        {county_query}
    """

    # Getting the data itself
    client = Socrata("data.pa.gov", PA_APP_TOKEN)
    results = client.get("etb6-jzdg", query=query)
    client.close()

    df = pd.DataFrame.from_records(results).fillna("N/A").rename(columns={
        'public_facility_name': "Name",
        'address': "Address",
        'city': "City",
        'inspection_date': "Inspection Date",
        'inspection_reason_type': "Reason For Inspection",
        'overall_compliance': "Passed Inspection",
    })
    df = df[['Passed Inspection', 'Name', 'Address', 'City', 'Inspection Date', 'Reason For Inspection']]

    if df.empty:
        return df

    df.drop_duplicates("Name", keep='last', inplace=True)
    df['Inspection Date'] = df['Inspection Date'].str.split('T').str.get(0)
    return df
