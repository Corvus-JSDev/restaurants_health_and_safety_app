import streamlit as st
from src import helpers

# Print the among us character
amongus = chr(sum(range(ord(min(str(not()))))))

print(f"\n----- Prerequisite Checks -----\n")
helpers.ensure_county_data_is_installed()
helpers.ensure_sql_database_exists()
print(f"\n----- Prerequisite Complete! -----\n")
