import os
from src import data_collection

current_directory = os.path.dirname(os.path.abspath(__file__))


def ensure_county_data_is_installed():
	file_path = f"{current_directory}/../data/processed/counties_with_states.csv"
	if not os.path.exists(file_path):
		print("\033[33m CSV data not found. Downloading data now... \033[0m")
		data_collection.download_list_of_counties()
		print("\033[32m  \u2713 Download complete. \033[0m")
	else:
		print("\033[32m  \u2713 County CSV found. \033[0m")


def ensure_sql_database_exists():
	file_path = f"{current_directory}/../data/sql_data/CountiesByState.db"
	if not os.path.exists(file_path):
		print('\033[33m SQL database not found. Creating database... \033[0m')
		data_collection.create_sql_database()
		print('\033[32m  \u2713 Database created. \033[0m')
	else:
		print("\033[32m  \u2713 SQL Database found. \033[0m")
