import os
import pandas as pd
from . import data_collection
import sqlite3
import geocoder  # NOTE: For some reason pyright is saying this could not be resolved, even tho it works perfectly fine... i hate pyright.

list_of_supported_states = sorted(['new york', 'pennsylvania'])

color_red = '#fc5050'
color_orange = '#fcbc4e'
color_green = '#3edd60'
color_default = "#d0ccc6"



current_directory = os.path.dirname(os.path.abspath(__file__))
path_to_db = f"{current_directory}/../data/sql_data/CountiesByState.db"
amongus_character = chr(sum(range(ord(min(str(not()))))))

def ensure_county_data_is_installed():
	file_path = f"{current_directory}/../data/processed/counties_with_states.csv"
	if not os.path.exists(file_path):
		print("\033[33m CSV data not found. Downloading data now... \033[0m")
		data_collection.download_list_of_counties()
		print("\033[32m  \u2713 Download complete. \033[0m")
	else:
		print("\033[32m  \u2713 County CSV found. \033[0m")


def ensure_sql_database_exists():
	if not os.path.exists(path_to_db):
		print('\033[33m SQL database not found. Creating database... \033[0m')
		data_collection.create_sql_database()
		print('\033[32m  \u2713 Database created. \033[0m')
	else:
		print("\033[32m  \u2713 SQL Database found. \033[0m")


def get_list_of_states():
	with sqlite3.connect(path_to_db) as connect:
		cursor = connect.cursor()
		cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
		list_of_states = cursor.fetchall()
	return [state[0] for state in list_of_states]


def get_list_of_counties(selected_state):
	with sqlite3.connect(path_to_db) as connect:
		cursor = connect.cursor()
		cursor.execute(f"SELECT * FROM \'{selected_state}\'")
		list_of_counties = cursor.fetchall()
	return [county[0] for county in list_of_counties]


def loc_state():
	list_of_states = get_list_of_states()
	g = geocoder.ip('me')
	state_name = g.state if g.ok else None
	return next((index for index, state in enumerate(list_of_states) if state == state_name), None)


def ny_color_column(score):
	if score == 'N/A':
		return f'color: {color_default};'

	try:
		score = float(score)
	except ValueError:
		return f'color: {color_default};'

	if score >= 6:
		color = color_red
	elif score >= 4:
		color = color_orange
	else:
		color = color_green
	return f'color: {color};'


def pa_color_column(passed):
	if passed == 'Yes':
		color = color_green
	elif passed == 'No':
		color = color_red
	else:
		color = color_default

	return f'color: {color};'


def highlight_alternate_rows(row):
	return ['background-color: #1c1f28' if i % 2 == 0 else 'background-color: #242833' for i in range(len(row))]






if __name__ == "__main__":
	print('RUNNING: helpers.py\n')
	print('-------------------\n')
