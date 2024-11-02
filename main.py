import streamlit as st
from src import helpers

print("\n----- Prerequisite Checks -----\n")
helpers.ensure_county_data_is_installed()
helpers.ensure_sql_database_exists()
print("\n----- Prerequisite Complete! -----\n")
