import pandas as pd
import os
import sqlite3
from src import styling
from sodapy import Socrata
from datetime import date
from dateutil.relativedelta import relativedelta
from dotenv import load_dotenv
load_dotenv()

current_directory = os.path.dirname(os.path.abspath(__file__))





NY_APP_TOKEN = os.getenv('NY_APP_TOKEN') or None
def get_NY_health_inspection_data(county, resturant_name=''):
	county = county.split()[0].upper()
	resturant_query = f'AND facility == \'{resturant_name}\'' if resturant_name else ''
	county_query = f'county == \'{county}\'' if county else ''

	query = f"""
	SELECT
	    *
	WHERE
		{county_query}
	LIMIT
		20000
	"""

	# Getting the data itself
	client = Socrata("health.data.ny.gov", NY_APP_TOKEN)
	results = client.get("cnih-y5dw", query=query)
	client.close()

	df = pd.DataFrame.from_records(results)

	# This is here because for some reason NY doesn't want to share their data for some counties. Can you tell I hate working with gov APIs yet? Like honestly, how hard is it to have data for all of YOUR OWN counties?
	if df.empty:
		return df


	# Formatting
	df['Number Of Inspections'] = 1
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
	    'date': 'Earliest Recorded Inspection (Y-M-D)',
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
	df['Earliest Recorded Inspection (Y-M-D)'] = df['Earliest Recorded Inspection (Y-M-D)'].str.split('T').str.get(0)

	# Moves the risk score and name column to the front
	cols = ['Risk Score', 'Name'] + [col for col in df.columns if col != 'Risk Score' and col != 'Name']
	df = df[cols]

	# Style the df
	styled_df = df.style.map(styling.ny_color_column, subset=['Risk Score'])

	return styled_df





PA_APP_TOKEN = os.getenv('PA_APP_TOKEN') or None
def get_PA_health_inspection_data(county, resturant_name=''):
	county = county.split()[0].title()
	county_query = f'county_name == \'{county}\'' if county else ''
	resturant_query = f'AND facility == \'{resturant_name}\'' if resturant_name else ''

	query = f"""
	SELECT
		*
	WHERE
		{county_query}
	LIMIT
		50000
	"""

	# Getting the data itself
	client = Socrata("data.pa.gov", PA_APP_TOKEN)
	results = client.get("etb6-jzdg", query=query)
	client.close()

	df = pd.DataFrame.from_records(results)
	if df.empty:
		return df

	# Filling nulls and renaming
	df = df.fillna("N/A").rename(columns={
		'public_facility_name': "Name",
		'address': "Address",
		'city': "City",
		'inspection_date': "Inspection Date",
		'inspection_reason_type': "Reason For Inspection",
		'overall_compliance': "Passed Inspection",
	})

	# Formatting
	df = df[['Passed Inspection', 'Name', 'Address', 'City', 'Inspection Date', 'Reason For Inspection']]
	df.drop_duplicates(subset=['Address'], keep='last', inplace=True)
	df['Inspection Date'] = df['Inspection Date'].str.split('T').str.get(0)

	# Styling
	styled_df = df.style.map(styling.pa_color_column, subset=['Passed Inspection'])

	return styled_df





# Sign up for an app token here: https://data.delaware.gov/profile/edit/developer_settings
DE_APP_TOKEN = os.getenv('DE_APP_TOKEN') or None
def get_DE_health_inspection_data(city=''):
	query = f"""
	SELECT
		*
	WHERE
		insp_date > {str(date.today() - relativedelta(years=2))}T00:00:00.000
	LIMIT
		30000
	"""

	# Getting the data itself
	client = Socrata("data.delaware.gov", DE_APP_TOKEN)
	results = client.get("384s-wygj")
	client.close()

	df = pd.DataFrame.from_records(results)
	if df.empty:
		return df

	# Filtering by city
	if city:
		df = df.loc[ df['restcity'] == city ]

	# Formatting
	df = df.fillna("N/A").rename(columns={
		'restname': 'Name',
		'restaddress': 'Address',
		'restcity': 'City',
		'insp_date': 'Earliest Recorded Inspection',
		'violation': 'Violation Code(s)',
		'vio_desc': 'Description',
	}).drop(columns=['geocoded_column', 'restzip', 'insp_type'])
	df['Total Violations'] = 1
	df['Earliest Recorded Inspection'] = df['Earliest Recorded Inspection'].str.split('T').str.get(0)

	# Grouping
	df = df.groupby('Address').agg({
		'Name': 'first',
		'City': 'first',
		'Earliest Recorded Inspection': 'min',
		'Violation Code(s)': list,
		'Description': list,
		'Total Violations': 'sum'
	}).reset_index()

	# Even more formatting
	df['Violation Code(s)'] = df['Violation Code(s)'].apply(lambda x: ' | '.join(x))
	df['Description'] = df['Description'].apply(lambda x: ' | '.join(x))

	# Move this column to the front
	cols = ['Total Violations'] + [col for col in df.columns if col != 'Total Violations']
	df = df[cols]

	# Styling
	styled_df = df.style.map(styling.de_color_column, subset=['Total Violations'])

	return styled_df
