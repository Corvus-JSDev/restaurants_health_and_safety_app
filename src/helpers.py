import os
from src import data_collection

def ensure_county_data_is_installed():
	current_directory = os.path.dirname(os.path.abspath(__file__))
	file_path = f"{current_directory}/../data/processed/counties_with_states.csv"
	if not os.path.exists(file_path):
		print("data not installed")
		data_collection.download_list_of_counties()
	else:
		print("nothing to do")
